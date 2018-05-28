import argparse
import nltk
import pdb
import sys, os
from collections import defaultdict
import random

def read_ids(test_ids_fname):
  test_ids = [line.strip('\n') for line in open(test_ids_fname, 'r').readlines()]
  return test_ids

def read_model_outputs(model_fname, model_test_ids_fname):
  model_test_ids = read_ids(model_test_ids_fname)
  with open(model_fname, 'r') as model_file:
    model_outputs = [line.strip('\n') for line in model_file.readlines()]
  assert(len(model_test_ids) == len(model_outputs))
  model_output_dict = defaultdict(list)
  for i, test_id in enumerate(model_test_ids):
    asin = test_id.split('_')[0]
    model_output_dict[asin].append(model_outputs[i])
  return model_output_dict

def main(args):
    test_ids = read_ids(args.test_ids)
    model_outs = read_model_outputs(args.model_outputs, args.model_test_ids)
    model_outputs_perid = open(args.model_outputs_perid, 'w')
    for asin in test_ids:
      try:
        question = random.choice(model_outs[asin])
      except:
        print asin
        question = ''
      model_outputs_perid.write(question+'\n')
    model_outputs_perid.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--test_ids", type=str)
    argparser.add_argument("--model_outputs", type=str)
    argparser.add_argument("--model_test_ids", type=str)
    argparser.add_argument("--model_outputs_perid", type=str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)

