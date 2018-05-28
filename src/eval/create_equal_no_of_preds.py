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
  model_output_dict = defaultdict(list)
  for i, test_id in enumerate(model_test_ids):
    asin = test_id.split('_')[0]
    model_output_dict[asin].append(model_outputs[i])
  return model_output_dict

def main(args):
    model_outs = read_model_outputs(args.model_outputs, args.model_test_ids)
    new_model_outs_file = open(args.new_model_outputs, 'w')
    for asin in model_outs:
      c = len(model_outs[asin])
      for i in range(c):
        question = model_outs[asin][i]
        new_model_outs_file.write(question+'\n')
      for j in range(c, 20):
        question = random.choice(model_outs[asin])
        new_model_outs_file.write(question+'\n')
    new_model_outs_file.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--model_outputs", type=str)
    argparser.add_argument("--model_test_ids", type=str)
    argparser.add_argument("--new_model_outputs", type=str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)