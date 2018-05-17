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

def main(args):
    titles = {}
    descriptions = {}
    test_ids = read_ids(args.test_ids)
    onlycontext_model_outs = read_model_outputs(args.onlycontext_model, args.onlycontext_model_test_ids)
    simcandqs_model_outs = read_model_outputs(args.simcandqs_model, args.simcandqs_model_test_ids)
    simcandqs_template_model_outs = read_model_outputs(args.simcandqs_template_model, args.simcandqs_template_model_test_ids)
    for v in parse(args.metadata_fname):
        asin = v['asin']
        if asin not in test_ids:
          continue
        if asin not in onlycontext_model_outs or \
          asin not in simcandqs_model_outs or \
          asin not in simcandqs_template_model_outs:
          continue
        description = v['description']
        length = len(description.split())
        title = v['title']
        if length >= 100 or length < 10 or len(title.split()) == length:
          continue
        titles[asin] = title
        descriptions[asin] = description
        if len(descriptions) >= 500:
          break

    questions = defaultdict(list)
    for v in parse(args.qa_data_fname):
        asin = v['asin']
        if asin not in descriptions:
            continue
        questions[asin].append(v['question'])
    
    csv_file = open(args.csv_file, 'w')
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['title', 'description', 'q1_model', 'q1', 'q2_model', 'q2', 'q3_model', 'q3', 'q4_model', 'q4'])
    for asin in descriptions:
      title = titles[asin]
      description = descriptions[asin]
      ques_candidates = []
      for ques in questions[asin]:
        if len(ques.split()) > 30:
          continue
        ques_candidates.append(ques)
      if len(ques_candidates) == 0:
        pdb.set_trace()
      gold_question = random.choice(ques_candidates)
      onlycontext_question = random.choice(onlycontext_model_outs[asin])
      simcandqs_question = random.choice(simcandqs_model_outs[asin])
      simcandqs_template_question = random.choice(simcandqs_template_model_outs[asin])
      pairs = [('gold', gold_question), ('onlycontext', onlycontext_question), \
                ('simcandqs', simcandqs_question), ('simcandqs_template', simcandqs_template_question)]
      random.shuffle(pairs)
      writer.writerow([title, description, \
                       pairs[0][0], pairs[0][1], pairs[1][0], pairs[1][1], \
                        pairs[2][0], pairs[2][1], pairs[3][0], pairs[3][1]])
    csv_file.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--qa_data_fname", type = str)
    argparser.add_argument("--metadata_fname", type = str)
    argparser.add_argument("--test_ids", type=str)
    argparser.add_argument("--csv_file", type=str)
    argparser.add_argument("--onlycontext_model", type=str)
    argparser.add_argument("--onlycontext_model_test_ids", type=str)
    argparser.add_argument("--simcandqs_model", type=str)
    argparser.add_argument("--simcandqs_model_test_ids", type=str)
    argparser.add_argument("--simcandqs_template_model", type=str)
    argparser.add_argument("--simcandqs_template_model_test_ids", type=str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)

