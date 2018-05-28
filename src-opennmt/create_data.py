import argparse
import sys, os
from collections import defaultdict
import csv
import math
import pdb
import random
import numpy as np

MAX_POST_LEN=200
MAX_QUES_LEN=40
#MIN_TFIDF=30
MIN_TFIDF=2
MIN_QUES_TFIDF=2000
#MAX_QUES_TFIDF=8
MAX_QUES_TFIDF=10

def write_to_file(ids, args, posts, question_candidates, template_question_candidates, sim_ques, split, candqs_list=None):
	suffix = ''
	if args.nocontext:
		suffix += '_nocontext'
	if args.simqs:
		suffix += '_simqs'
	if args.candqs:
		suffix += '_candqs'
	if args.template:
		suffix += '_template'
	if args.onlycontext:
		suffix += '_onlycontext'
	suffix += '.txt'

	if split == 'train':
		src_file = open(args.train_src_fname+suffix, 'w')
		tgt_file = open(args.train_tgt_fname+suffix, 'w')
	elif split == 'tune':
		src_file = open(args.tune_src_fname+suffix, 'w')
		tgt_file = open(args.tune_tgt_fname+suffix, 'w')
	if split == 'test':
		src_file = open(args.test_src_fname+suffix, 'w')
		tgt_file = open(args.test_tgt_fname+suffix, 'w')
		if not candqs_list:
			test_candqs_list_file = open(args.test_candqs_list_fname, 'w')
			
	if not candqs_list:
		candqs_list = [None]*len(ids)
	for k, post_id in enumerate(ids):
		src_line = ''
		if not args.nocontext:
			src_line += posts[post_id]+' <EOP> '
		if not candqs_list[k]:
			random_list = range(1,10)
			random.shuffle(random_list)
			candqs_list[k] = random_list[:3]
			if split == 'test':
				test_candqs_list_file.write(' '.join([str(s) for s in candqs_list[k]])+'\n')
		if args.candqs:
			for i in range(3):
				if args.template:
					src_line += template_question_candidates[post_id][candqs_list[k][i]]+' <EOQ> '
				else:
					src_line += question_candidates[post_id][candqs_list[k][i]]+' <EOQ> '
		if args.simqs:
			i = 1
			n = 0
			while n < 3 and i < 10:
				try:
					if args.template:
						src_line += template_question_candidates[sim_ques[post_id][i]][0]+' <EOQ> '
					else:
						src_line += question_candidates[sim_ques[post_id][i]][0]+' <EOQ> '				
					i += 1
					n += 1
				except:
					i += 1
		# i = 1
		# n = 0
		# while n < 3 and i < 10:
		# 	try:
		# 		if args.simqs:
		# 			if args.template:
		# 				src_line += template_question_candidates[sim_ques[post_id][i]][0]+' <EOQ> '
		# 			else:
		# 				src_line += question_candidates[sim_ques[post_id][i]][0]+' <EOQ> '
		# 		if args.candqs:
		# 			if args.template:
		# 				src_line += template_question_candidates[post_id][i]+' <EOQ> '
		# 			else:
		# 				src_line += question_candidates[post_id][i]+' <EOQ> '
		# 		i += 1
		# 		n += 1
		# 	except:
		# 		i += 1
		src_file.write(src_line+'\n')	
		tgt_file.write(question_candidates[post_id][0]+'\n')
	
	src_file.close()
	tgt_file.close()

def get_sim_ques(sim_ques_filename):
	sim_ques_file = open(sim_ques_filename, 'r')
	sim_ques = {}
	for line in sim_ques_file.readlines():
		parts = line.split()
		if len(parts) > 1:
			sim_ques[parts[0]] = parts[1:]
		else:
			sim_ques[parts[0]] = []
	return sim_ques

def trim_by_len(s, max_len):
	s = s.lower().strip()
	words = s.split()
	s = ' '.join(words[:max_len])
	return s

def trim_by_tfidf(posts, p_tf, p_idf):
	for post_id in posts:
		post = []
		words = posts[post_id].split()
		for w in words:
			tf = words.count(w)
			#if p_tf[w]*p_idf[w] >= MIN_TFIDF:
			if tf*p_idf[w] >= MIN_TFIDF:
				post.append(w)
			if len(post) >= MAX_POST_LEN:
				break
		posts[post_id] = ' '.join(post)
	return posts

def has_number(string):
	for char in string:
		if char.isdigit():
			return True
	return False

def template_by_tfidf(question_candidates, q_tf, q_idf):
	template_question_candidates = {}
	for post_id in question_candidates:
		template_question_candidates[post_id] = []
		for i, ques in enumerate(question_candidates[post_id]):
			template_ques = []
			words = ques.split()
			for w in words:
				tf = words.count(w)
				#if q_tf[w]*q_idf[w] >= MIN_QUES_TFIDF or w == '?':
				if has_number(w) or tf*q_idf[w] > MAX_QUES_TFIDF:
					template_ques.append('<BLANK>')
				else:
					template_ques.append(w)
			template_question_candidates[post_id].append(' '.join(template_ques))
	return template_question_candidates

def read_test_candqs_list(test_candqs_list_fname):
	test_candqs_list = []
	for line in open(test_candqs_list_fname, 'r').readlines():
		line = line.strip('\n')
		test_candqs_list.append([int(c) for c in line.split()])
	return test_candqs_list

def read_data(args):
	print("Reading lines...")
	posts = {}
	question_candidates = {}
	p_tf = defaultdict(int)
	p_idf = defaultdict(int)
	with open(args.post_data_tsvfile, 'rb') as tsvfile:
		post_reader = csv.reader(tsvfile, delimiter='\t')
		N = 0
		for row in post_reader:
			if N == 0:
				N += 1
				continue
			N += 1
			post_id,title,post = row
			post = title + ' ' + post
			post = post.lower().strip()
			for w in post.split():
				p_tf[w] += 1
			for w in set(post.split()):
				p_idf[w] += 1	
			posts[post_id] = post 

	for w in p_idf:
		p_idf[w] = math.log(N*1.0/p_idf[w])

	posts = trim_by_tfidf(posts, p_tf, p_idf)
	sim_ques = get_sim_ques(args.sim_ques_fname)	

	no_sim_ques = 0
	q_tf = defaultdict(int)
	q_idf = defaultdict(int)
	N = 0
	with open(args.qa_data_tsvfile, 'rb') as tsvfile:
		qa_reader = csv.reader(tsvfile, delimiter='\t')
		i = 0
		for row in qa_reader:
			if i == 0:
				i += 1
				continue
			post_id,questions = row[0], row[1:11]
			questions = [trim_by_len(question, MAX_QUES_LEN) for question in questions]
			question_candidates[post_id] = questions
			for ques in questions:
				N += 1
				for w in ques.split():
					q_tf[w] += 1
				for w in set(ques.split()):
					q_idf[w] += 1

	for w in q_idf:
		q_idf[w] = math.log(N*1.0/q_idf[w])

	template_question_candidates = template_by_tfidf(question_candidates, q_tf, q_idf)	

	train_ids = [train_id.strip('\n') for train_id in open(args.train_ids_file, 'r').readlines()]
	tune_ids = [tune_id.strip('\n') for tune_id in open(args.tune_ids_file, 'r').readlines()]
	test_ids = [test_id.strip('\n') for test_id in open(args.test_ids_file, 'r').readlines()]
	
	if os.path.exists(args.test_candqs_list_fname):
		test_candqs_list = read_test_candqs_list(args.test_candqs_list_fname)
	else:
		test_candqs_list = None
	
	write_to_file(train_ids, args, posts, question_candidates, template_question_candidates, sim_ques, 'train')	
	write_to_file(tune_ids, args, posts, question_candidates, template_question_candidates, sim_ques, 'tune')	
	write_to_file(test_ids, args, posts, question_candidates, template_question_candidates, sim_ques, 'test',test_candqs_list)	

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--post_data_tsvfile", type = str)
	argparser.add_argument("--qa_data_tsvfile", type = str)
	argparser.add_argument("--train_ids_file", type = str)
	argparser.add_argument("--train_src_fname", type = str)
	argparser.add_argument("--train_tgt_fname", type = str)
	argparser.add_argument("--tune_ids_file", type = str)
	argparser.add_argument("--tune_src_fname", type = str)
	argparser.add_argument("--tune_tgt_fname", type = str)
	argparser.add_argument("--test_ids_file", type = str)
	argparser.add_argument("--test_src_fname", type = str)
	argparser.add_argument("--test_tgt_fname", type = str)
	argparser.add_argument("--sim_ques_fname", type = str)
	argparser.add_argument("--test_candqs_list_fname", type = str)
	argparser.add_argument("--simqs", type = bool)
	argparser.add_argument("--candqs", type = bool)
	argparser.add_argument("--template", type = bool)
	argparser.add_argument("--nocontext", type = bool)
	argparser.add_argument("--onlycontext", type = bool)
	args = argparser.parse_args()
	print args
	print ""
	read_data(args)
	
