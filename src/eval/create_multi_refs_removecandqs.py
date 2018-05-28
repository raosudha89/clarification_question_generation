import argparse
import csv
import sys, os, pdb
import nltk
import time
import random
from nltk.translate.bleu_score import SmoothingFunction
chencherry = SmoothingFunction()

MAX_REF_COUNT=6

def get_annotations(line):
	set_info, post_id, best, valids, confidence = line.split(',')
	annotator_name = set_info.split('_')[0]
	sitename = set_info.split('_')[1]
	best = int(best)
	valids = [int(v) for v in valids.split()]
	confidence = int(confidence)
	return post_id, annotator_name, sitename, best, valids, confidence

def read_human_annotations(human_annotations_filename):
	human_annotations_file = open(human_annotations_filename, 'r')
	annotations = {}
	for line in human_annotations_file.readlines():
		line = line.strip('\n')
		splits = line.split('\t')
		post_id1, annotator_name1, sitename1, best1, valids1, confidence1 = get_annotations(splits[0])
		post_id2, annotator_name2, sitename2, best2, valids2, confidence2 = get_annotations(splits[1])		
		assert(sitename1 == sitename2)
		assert(post_id1 == post_id2)
		post_id = sitename1+'_'+post_id1
		best_union = list(set([best1, best2]))
		valids_inter = list(set(valids1).intersection(set(valids2)))
		annotations[post_id] = list(set(best_union + valids_inter))
	return annotations

def create_refs(test_ids, annotations, question_candidates, test_candqs_list, ref_prefix):
	ref_files = [None]*MAX_REF_COUNT
	for i in range(MAX_REF_COUNT):
		ref_files[i] = open(ref_prefix+str(i), 'w')

	for i, post_id in enumerate(test_ids):
		if post_id not in annotations:
			continue
		refs = []
		for v in test_candqs_list[i]:
			if v in annotations[post_id]: annotations[post_id].remove(v)
		if len(annotations[post_id]) == 0:
			print post_id
			annotations[post_id].append(test_candqs_list[i][0])
		for j, ques_no in enumerate(annotations[post_id]):
			ref = question_candidates[post_id][ques_no]
			refs.append(ref)
			ref_files[j].write(ref+'\n')
		for k in range(len(refs), MAX_REF_COUNT):
			r = random.randint(0, len(refs)-1)
			ref_files[k].write(refs[r]+'\n')

def main(args):
	question_candidates = {}
	test_ids = [test_id.strip('\n') for test_id in open(args.test_ids_file, 'r').readlines()]

	test_candqs_list = []
	with open(args.test_candqs_list_file, 'r') as test_candqs_list_file:
		lines = test_candqs_list_file.readlines()
		for line in lines:
			line = line.strip('\n')
			test_candqs_list.append([int(v) for v in line.split()])

	with open(args.qa_data_tsvfile, 'rb') as tsvfile:
		qa_reader = csv.reader(tsvfile, delimiter='\t')
		i = 0
		for row in qa_reader:
			if i == 0:
				i += 1
				continue
			post_id,questions = row[0], row[1:11]
			question_candidates[post_id] = questions

	annotations = read_human_annotations(args.human_annotations)
	create_refs(test_ids, annotations, question_candidates, test_candqs_list, args.ref_prefix)	

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--qa_data_tsvfile", type = str)
	argparser.add_argument("--human_annotations", type = str)
	argparser.add_argument("--test_candqs_list_file", type = str)
	argparser.add_argument("--test_ids_file", type = str)
	argparser.add_argument("--ref_prefix", type = str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)

