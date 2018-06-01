import argparse
import gzip
import nltk
import pdb
import sys, os
from collections import defaultdict
import csv
import random

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)

def read_ids(fname):
  return [line.strip('\n') for line in open(fname, 'r').readlines()]

def read_model_outputs(model_fname, model_test_ids_fname):
  model_test_ids = read_ids(model_test_ids_fname)
  with open(model_fname, 'r') as model_file:
    model_outputs = [line.strip('\n') for line in model_file.readlines()]
  model_output_dict = defaultdict(list)
  for i, test_id in enumerate(model_test_ids):
    asin = test_id.split('_')[0]
    model_output_dict[asin].append(model_outputs[i])
  return model_output_dict

def get_subset(candidates):
  print len(candidates)
  new_candidates = []
  for cand in candidates:
    if len(cand.split()) <= 50:
      new_candidates.append(cand)
  print len(new_candidates)
  if len(new_candidates) == 0:
    pdb.set_trace()
  return new_candidates

def main(args):
    titles = {}
    descriptions = {}
    test_ids = read_ids(args.test_ids)
    lucene_model_outs = read_model_outputs(args.lucene_model, args.lucene_model_test_ids)
    context_model_outs = read_model_outputs(args.context_model, args.context_model_test_ids)
    candqs_model_outs = read_model_outputs(args.candqs_model, args.candqs_model_test_ids)
    candqs_template_model_outs = read_model_outputs(args.candqs_template_model, \
                                                       args.candqs_template_model_test_ids)
    for v in parse(args.metadata_fname):
        asin = v['asin']
        if asin not in test_ids:
          continue
        if asin not in lucene_model_outs or \
            asin not in context_model_outs or \
            asin not in candqs_model_outs or \
            asin not in candqs_template_model_outs:
              continue
        description = v['description']
        length = len(description.split())
        title = v['title']
        if length >= 100 or length < 10 or len(title.split()) == length:
          continue
        titles[asin] = title
        descriptions[asin] = description
        if len(descriptions) >= 100:
          break

    print len(descriptions)
    questions = defaultdict(list)
    for v in parse(args.qa_data_fname):
        asin = v['asin']
        if asin not in descriptions:
            continue
        questions[asin].append(v['question'])
    
    csv_file = open(args.csv_file, 'w')
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['asin', 'title', 'description', \
                        'q1_model', 'q1', 'q2_model', 'q2', \
                        'q3_model', 'q3', 'q4_model', 'q4', \
                        'q5_model', 'q5'])
    all_rows = []
    for asin in descriptions:
      title = titles[asin]
      description = descriptions[asin]
      #ques_candidates = []
      #for ques in questions[asin]:
      #  if len(ques.split()) > 30:
      #    continue
      #  ques_candidates.append(ques)
      gold_question = random.choice(questions[asin])
      lucene_question = random.choice(lucene_model_outs[asin])
      context_question = random.choice(context_model_outs[asin])
      candqs_question = random.choice(candqs_model_outs[asin])
      candqs_template_question = random.choice(candqs_template_model_outs[asin])
      pairs = [('gold', gold_question), ('lucene', lucene_question), \
                ('context', context_question), ('candqs', candqs_question), \
                ('candqs_template', candqs_template_question)]
      random.shuffle(pairs)
      writer.writerow([asin, title, description, \
                        pairs[0][0], pairs[0][1], pairs[1][0], pairs[1][1], \
                        pairs[2][0], pairs[2][1], pairs[3][0], pairs[3][1], \
                        pairs[4][0], pairs[4][1]])      
    
    csv_file.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--qa_data_fname", type = str)
    argparser.add_argument("--metadata_fname", type = str)
    argparser.add_argument("--test_ids", type=str)
    argparser.add_argument("--csv_file", type=str)
    argparser.add_argument("--lucene_model", type=str)
    argparser.add_argument("--lucene_model_test_ids", type=str)
    argparser.add_argument("--context_model", type=str)
    argparser.add_argument("--context_model_test_ids", type=str)
    argparser.add_argument("--candqs_model", type=str)
    argparser.add_argument("--candqs_model_test_ids", type=str)
    argparser.add_argument("--candqs_template_model", type=str)
    argparser.add_argument("--candqs_template_model_test_ids", type=str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)

