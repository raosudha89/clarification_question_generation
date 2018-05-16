import argparse
import csv
import sys, os, pdb
import nltk
import time
from nltk.translate.bleu_score import SmoothingFunction
chencherry = SmoothingFunction()

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
		#annotations[post_id] = best_union
		#annotations[post_id] = [0]
	return annotations

def calculate_bleu(test_ids, annotations, question_candidates, model_outputs, model_name):
	total_BLEUscore = 0
	total_mosesBLEUscore = 0
	total_mosesBLEUscore1 = 0
	total_mosesBLEUscore2 = 0
	total_mosesBLEUscore3 = 0
	total_mosesBLEUscore4 = 0
	total_meteor_score = 0
	assert(len(test_ids) == len(model_outputs))
	timestr = time.strftime("%Y%m%d-%H%M%S")
	tmpdirname = 'bleu_'+model_name+timestr
	os.system('mkdir %s' % tmpdirname)
	for i, post_id in enumerate(test_ids):
		if post_id not in annotations:
			continue
		hyp = model_outputs[i].split()
		timestr = time.strftime("%Y%m%d-%H%M%S")
		with open(os.path.join(tmpdirname, "hyp."+timestr), 'w') as hyp_f:
			hyp_f.write(' '.join(hyp)+'\n')
		refs = []
		BLEUscore = 0.0
		ref_file_list = ''
		for j, ques_no in enumerate(annotations[post_id]):
			ref = question_candidates[post_id][ques_no].split()
			with open(os.path.join(tmpdirname, "ref."+timestr+'.'+str(j)), 'w') as ref_f:
				ref_f.write(' '.join(ref)+'\n')
			refs.append(ref)
			ref_file_list += '%s/ref.%s.%s ' % (tmpdirname, timestr, str(j))
			#BLEUscore = max(BLEUscore, nltk.translate.bleu_score.sentence_bleu([ref], hyp, smoothing_function=chencherry.method2))
		BLEUscore = nltk.translate.bleu_score.sentence_bleu(refs, hyp, smoothing_function=chencherry.method2)
		#BLEUscore = nltk.translate.bleu_score.sentence_bleu(refs, hyp)
		total_BLEUscore += BLEUscore
		os.system("perl /fs/clip-software/user-supported/mosesdecoder/3.0/scripts/generic/multi-bleu.perl \
						%s/ref.%s. < %s/hyp.%s > %s/bleu_score.%s" % (tmpdirname, timestr, tmpdirname, timestr, tmpdirname, timestr))
		mosesBLEUscore_line = open(os.path.join(tmpdirname, "bleu_score.%s" % timestr), 'r').readline().strip('\n')
		mosesBLEUscore = float(mosesBLEUscore_line.split()[2][:-1])
		mosesBLEUscore1, mosesBLEUscore2, mosesBLEUscore3, mosesBLEUscore4 = [float(s) for s in mosesBLEUscore_line.split()[3].split('/')]
		total_mosesBLEUscore += mosesBLEUscore
		total_mosesBLEUscore1 += mosesBLEUscore1
		total_mosesBLEUscore2 += mosesBLEUscore2
		total_mosesBLEUscore3 += mosesBLEUscore3
		total_mosesBLEUscore4 += mosesBLEUscore4

		os.system("java -Xmx2G -jar /fs/clip-software/user-supported/meteor-1.5/meteor-1.5.jar %s/hyp.%s %s -l en -norm -q > %s/meteor_score.%s" \
																					% (ref_file_list, tmpdirname, timestr, tmpdirname, timestr))
		meteor_score = float(open(os.path.join(tmpdirname, "meteor_score.%s" % timestr), 'r').readline().strip('\n'))
		total_meteor_score += meteor_score
		os.system("rm %s/hyp.%s %s/ref.%s.* %s/bleu_score.%s" % (tmpdirname, timestr, tmpdirname, timestr, tmpdirname, timestr))

	print 'NLTK BLEU %.3f' % (total_BLEUscore*1.0/len(annotations))
	print 'Moses BLEU %.3f' % (total_mosesBLEUscore*1.0/len(annotations))
	print 'Moses BLEU-1 %.3f' % (total_mosesBLEUscore1*1.0/len(annotations))
	print 'Moses BLEU-2 %.3f' % (total_mosesBLEUscore2*1.0/len(annotations))
	print 'Moses BLEU-3 %.3f' % (total_mosesBLEUscore3*1.0/len(annotations))
	print 'Moses BLEU-4 %.3f' % (total_mosesBLEUscore4*1.0/len(annotations))
	print 'Meteor %.3f' % (total_meteor_score*1.0/len(annotations))

	os.system('rm -r %s' % tmpdirname)

def main(args):
	question_candidates = {}
	model_outputs = []

	test_ids = [test_id.strip('\n') for test_id in open(args.test_ids_file, 'r').readlines()]

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
	model_output_file = open(args.model_output_file, 'r')
	for line in model_output_file.readlines():
		model_outputs.append(line.strip('\n'))

	calculate_bleu(test_ids, annotations, question_candidates, model_outputs, args.model_name)	

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--qa_data_tsvfile", type = str)
	argparser.add_argument("--human_annotations", type = str)
	argparser.add_argument("--model_output_file", type = str)
	argparser.add_argument("--test_ids_file", type = str)
	argparser.add_argument("--model_name", type = str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)

