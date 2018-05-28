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

def get_old_asins(old_aggregate_results):
  old_lucene_asins = []
  old_gold_asins = []
  old_simcandqs_asins = []
  with open(old_aggregate_results) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        if row['ques_model'] == 'lucene':
          old_lucene_asins.append(row['asin'])
        if row['ques_model'] == 'gold':
          old_gold_asins.append(row['asin'])
        if row['ques_model'] == 'simcandqs':
          old_simcandqs_asins.append(row['asin'])
  return list(set(old_lucene_asins)), list(set(old_gold_asins)), list(set(old_simcandqs_asins))

def main(args):
    titles = {}
    descriptions = {}
    test_ids = read_ids(args.test_ids)
    old_lucene_asins, old_gold_asins, old_simcandqs_asins = get_old_asins(args.old_aggregate_results)
    print len(old_lucene_asins)
    print len(old_gold_asins)
    print len(old_simcandqs_asins)
    lucene_model_outs = read_model_outputs(args.lucene_model, args.lucene_model_test_ids)
    #simcandqs_model_outs = read_model_outputs(args.simcandqs_model, args.simcandqs_model_test_ids)
    #simcandqs_template_model_outs = read_model_outputs(args.simcandqs_template_model, args.simcandqs_template_model_test_ids)
    for v in parse(args.metadata_fname):
        asin = v['asin']
        if asin not in test_ids:
          continue
        if asin not in lucene_model_outs:
          # or asin not in simcandqs_model_outs:
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
    writer.writerow(['asin', 'title', 'description', 'ques_model', 'ques'])
    all_rows = []
    
    for asin in descriptions:
      title = titles[asin]
      description = descriptions[asin]
      #ques_candidates = []
      #for ques in questions[asin]:
      #  if len(ques.split()) > 30:
      #    continue
      #  ques_candidates.append(ques)
      #if asin not in old_gold_asins:
      #  gold_question = random.choice(ques_candidates)
      #  all_rows.append([asin, title, description, 'gold', gold_question])
      if asin in old_lucene_asins:
        lucene_question = random.choice(lucene_model_outs[asin])
        all_rows.append([asin, title, description, 'lucene_new', lucene_question])
      #if asin not in old_simcandqs_asins:
      #  simcandqs_question = random.choice(simcandqs_model_outs[asin])
      #  all_rows.append([asin, title, description, 'simcandqs', simcandqs_question])
      #simcandqs_template_question = random.choice(simcandqs_template_model_outs[asin])
      #all_rows.append([asin, title, description, 'simcandqs_template', simcandqs_template_question])
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
    argparser.add_argument("--old_aggregate_results", type=str)
    argparser.add_argument("--lucene_model", type=str)
    argparser.add_argument("--lucene_model_test_ids", type=str)
    #argparser.add_argument("--simcandqs_model", type=str)
    #argparser.add_argument("--simcandqs_model_test_ids", type=str)
    #argparser.add_argument("--simcandqs_template_model", type=str)
    #argparser.add_argument("--simcandqs_template_model_test_ids", type=str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)

