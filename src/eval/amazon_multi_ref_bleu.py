import argparse
import csv
import sys, os, pdb
import nltk
import time
import random
from collections import defaultdict
from nltk.translate.bleu_score import SmoothingFunction
chencherry = SmoothingFunction()

def calculate_bleu(test_ids, question_candidates, model_outputs, model_name):
	total_BLEUscore = 0
	total_mosesBLEUscore = 0
	total_mosesBLEUscore1 = 0
	total_mosesBLEUscore2 = 0
	total_mosesBLEUscore3 = 0
	total_mosesBLEUscore4 = 0
	assert(len(test_ids) == len(model_outputs))
	timestr = time.strftime("%Y%m%d-%H%M%S")
	tmpdirname = 'bleu_'+model_name+timestr
	os.system('mkdir %s' % tmpdirname)
	mosesBLEUscores, mosesBLEUscores1, mosesBLEUscores2, mosesBLEUscores3, mosesBLEUscores4 = \
					defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
	for i, ques_id in enumerate(test_ids):
		hyp = model_outputs[i].split()
		timestr = time.strftime("%Y%m%d-%H%M%S")
		with open(os.path.join(tmpdirname, "hyp."+timestr), 'w') as hyp_f:
			hyp_f.write(' '.join(hyp)+'\n')
		asin = ques_id.split('_')[0]
		refs = [ques.split() for ques in question_candidates[asin]]
		for j, ref in enumerate(refs):
			with open(os.path.join(tmpdirname, "ref."+timestr+'.'+str(j)), 'w') as ref_f:
				ref_f.write(' '.join(ref)+'\n')
		BLEUscore = 0.0
		BLEUscore = nltk.translate.bleu_score.sentence_bleu(refs, hyp, smoothing_function=chencherry.method2)
		total_BLEUscore += BLEUscore
		os.system("perl /fs/clip-software/user-supported/mosesdecoder/3.0/scripts/generic/multi-bleu.perl \
					%s/ref.%s. < %s/hyp.%s > %s/bleu_score.%s" % (tmpdirname, timestr, tmpdirname, timestr, tmpdirname, timestr))
		mosesBLEUscore_line = open(os.path.join(tmpdirname, "bleu_score.%s" % timestr), 'r').readline().strip('\n')
		mosesBLEUscore = float(mosesBLEUscore_line.split()[2][:-1])
		mosesBLEUscore1, mosesBLEUscore2, mosesBLEUscore3, mosesBLEUscore4 = [float(s) for s in mosesBLEUscore_line.split()[3].split('/')]
		os.system("rm %s/hyp.%s %s/ref.%s.* %s/bleu_score.%s" % (tmpdirname, timestr, tmpdirname, timestr, tmpdirname, timestr))
		mosesBLEUscores[asin].append(mosesBLEUscore)
		mosesBLEUscores1[asin].append(mosesBLEUscore1)
		mosesBLEUscores2[asin].append(mosesBLEUscore2)
		mosesBLEUscores3[asin].append(mosesBLEUscore3)
		mosesBLEUscores4[asin].append(mosesBLEUscore4)

	os.system('rm -r %s' % tmpdirname)

	for asin in mosesBLEUscores:
		R = len(mosesBLEUscores[asin])
		for i in range(R, 10):
			j = random.randint(0, R-1) 
			mosesBLEUscores[asin].append(mosesBLEUscores[asin][j])
			mosesBLEUscores1[asin].append(mosesBLEUscores1[asin][j])
			mosesBLEUscores2[asin].append(mosesBLEUscores2[asin][j])
			mosesBLEUscores3[asin].append(mosesBLEUscores3[asin][j])
			mosesBLEUscores4[asin].append(mosesBLEUscores4[asin][j])
		total_mosesBLEUscore += sum(mosesBLEUscores[asin])/10
		total_mosesBLEUscore1 += sum(mosesBLEUscores1[asin])/10
		total_mosesBLEUscore2 += sum(mosesBLEUscores2[asin])/10
		total_mosesBLEUscore3 += sum(mosesBLEUscores3[asin])/10
		total_mosesBLEUscore4 += sum(mosesBLEUscores4[asin])/10

	N = len(mosesBLEUscores)
	print 'NLTK BLEU %.2f' % (total_BLEUscore*1.0/N)
	print 'Moses BLEU %.2f' % (total_mosesBLEUscore*1.0/N)
	print 'Moses BLEU-1 %.2f' % (total_mosesBLEUscore1*1.0/N)
	print 'Moses BLEU-2 %.2f' % (total_mosesBLEUscore2*1.0/N)
	print 'Moses BLEU-3 %.2f' % (total_mosesBLEUscore3*1.0/N)
	print 'Moses BLEU-4 %.2f' % (total_mosesBLEUscore4*1.0/N)

def main(args):
	question_candidates = {}
	model_outputs = []

	test_ids = [test_id.strip('\n') for test_id in open(args.test_ids_file, 'r').readlines()]

	for fname in os.listdir(args.ques_dir):
		with open(os.path.join(args.ques_dir, fname), 'r') as f:
			asin = fname[:-4].split('_')[0]
			if asin not in question_candidates:
				question_candidates[asin] = []
			if len(question_candidates[asin]) >= 5:
				continue
			ques = f.readline().strip('\n')
			question_candidates[asin].append(ques)
	
	model_output_file = open(args.model_output_file, 'r')
	for line in model_output_file.readlines():
		model_outputs.append(line.strip('\n'))

	calculate_bleu(test_ids, question_candidates, model_outputs, args.model_name)	

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--ques_dir", type = str)
	argparser.add_argument("--model_output_file", type = str)
	argparser.add_argument("--test_ids_file", type = str)
	argparser.add_argument("--model_name", type = str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)

