import argparse
import gzip
import nltk
import pdb
import sys, os
import re
from collections import defaultdict

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
	yield eval(l)

def preprocess(text):
	text = text.replace('|', ' ')
	text = text.replace('/', ' ')
	text = text.replace('\\', ' ')
	text = text.lower()
	#text = re.sub(r'\W+', ' ', text)
	ret_text = ''
	for sent in nltk.sent_tokenize(text):
		ret_text += ' '.join(nltk.word_tokenize(sent)) + ' '
	return ret_text

def main(args):
	asins = []
	datadump_file = open(args.datadump_fname, 'w')
	for v in parse(args.metadata_fname):
		if 'description' not in v or 'title' not in v:
			continue
		asin = v['asin']
		asins.append(asin)
		title = preprocess(v['title'])
		description = preprocess(v['description'])
		product = title + ' . ' + description + ' . '
		datadump_file.write(product)
	for v in parse(args.qa_data_fname):
		asin = v['asin']
		if asin not in asins:
			continue
		question = preprocess(v['question']) + ' . '
		answer = preprocess(v['answer']) + ' . '
		datadump_file.write(question + answer)
	datadump_file.close()

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--qa_data_fname", type = str)
	argparser.add_argument("--metadata_fname", type = str)
	argparser.add_argument("--datadump_fname", type = str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)

