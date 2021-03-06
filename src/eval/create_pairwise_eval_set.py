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
    lucene_model_outs = read_model_outputs(args.lucene_model, args.lucene_model_test_ids)
    simcandqs_model_outs = read_model_outputs(args.simcandqs_model, args.simcandqs_model_test_ids)
    for v in parse(args.metadata_fname):
        asin = v['asin']
        if asin not in test_ids:
          continue
        if asin not in lucene_model_outs or \
          asin not in simcandqs_model_outs:
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
    writer.writerow(['asin', 'title', 'description', 'q1_model', 'q1', 'q2_model', 'q2'])
    all_rows = []
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
      lucene_question = random.choice(lucene_model_outs[asin])
      simcandqs_question = random.choice(simcandqs_model_outs[asin])
      pairwise = [[('gold', gold_question), ('lucene', lucene_question)], \
                [('gold', gold_question), ('simcandqs', simcandqs_question)], \
                [('lucene', lucene_question), ('simcandqs', simcandqs_question)]]
      
      for i in range(3):
        random.shuffle(pairwise[i])
        #writer.writerow([asin, title, description, \
        #               pairwise[i][0][0], pairwise[i][0][1], \
        #                pairwise[i][1][0], pairwise[i][1][1]])
        all_rows.append([asin, title, description, \
                        pairwise[i][0][0], pairwise[i][0][1], \
                        pairwise[i][1][0], pairwise[i][1][1]])
    
    random.shuffle(all_rows)
    
    for row in all_rows:
      writer.writerow(row)
    
    csv_file.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--qa_data_fname", type = str)
    argparser.add_argument("--metadata_fname", type = str)
    argparser.add_argument("--test_ids", type=str)
    argparser.add_argument("--csv_file", type=str)
    argparser.add_argument("--lucene_model", type=str)
    argparser.add_argument("--lucene_model_test_ids", type=str)
    argparser.add_argument("--simcandqs_model", type=str)
    argparser.add_argument("--simcandqs_model_test_ids", type=str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)

