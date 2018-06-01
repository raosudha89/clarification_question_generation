import argparse
import csv
import sys
import numpy as np
from nltk.util import ngrams
import pdb
from collections import defaultdict

model_names = ['gold', 'lucene_new', 'simcandqs', 'lucene']
model_scores = {'gold':[], 'lucene_new':[], 'simcandqs':[], 'lucene':[]}

on_topic_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}, 'lucene':{}}
is_specific_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}, 'lucene':{}}
new_info_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}, 'lucene':{}}
customer_support_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}, 'lucene':{}}
useful_to_another_buyer_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}, 'lucene':{}}

on_topic_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[], 'lucene':[]}
is_specific_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[], 'lucene':[]}
new_info_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[], 'lucene':[]}
customer_support_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[], 'lucene':[]}
useful_to_another_buyer_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[], 'lucene':[]}

on_topic_levels = {'Strongly Agree': 3, 'Agree': 2, 'Disagree': 1, 'Strongly Disagree': 0}
is_specific_levels = {'Strongly Agree': 3, 'Agree': 2, 'Disagree': 1, 'Strongly Disagree': 0}
new_info_levels = {'Completely': 2, 'Somewhat': 1, 'No': 0}
customer_support_levels = {'Yes': 1, 'No': 0}
useful_to_another_buyer_levels = {'Strongly Agree': 3, 'Agree': 2, 'Disagree': 1, 'Strongly Disagree': 0}

def main(args):
    questions = {'gold': {}, 'lucene_new': {}, 'simcandqs': {}, 'lucene':{}}
    asin_model = []
    gold_asin_model = defaultdict(list)
    with open(args.full_results) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asin = row['asin']
            ques_model = row['ques_model']
            if row['_golden'] == 'true':
                gold_asin_model[asin].append(ques_model)
                continue
            if ques_model not in model_names:
                continue
            if (asin, ques_model) not in asin_model:
                on_topic_scores[ques_model][asin] = []
                is_specific_scores[ques_model][asin] = []
                new_info_scores[ques_model][asin] = []
                customer_support_scores[ques_model][asin] = []
                useful_to_another_buyer_scores[ques_model][asin] = []
                asin_model.append((asin, ques_model))
            ques = row['ques']
            on_topic = row['on_topic']
            is_specific = row['is_specific']
            new_info = row['new_info']
            customer_support = row['customer_support']
            useful_to_another_buyer = row['useful_to_another_buyer']
            
            on_topic_scores[ques_model][asin].append(on_topic_levels[on_topic])
            is_specific_scores[ques_model][asin].append(is_specific_levels[is_specific])
            new_info_scores[ques_model][asin].append(new_info_levels[new_info])
            customer_support_scores[ques_model][asin].append(customer_support_levels[customer_support])
            useful_to_another_buyer_scores[ques_model][asin].append(useful_to_another_buyer_levels[useful_to_another_buyer])

    with open(args.full_results_v4) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asin = row['asin']
            ques_model = row['ques_model']
            if row['_golden'] == 'true':
                gold_asin_model[asin].append(ques_model)
                continue
            if ques_model != 'lucene_new':
                continue
            if (asin, ques_model) not in asin_model:
                on_topic_scores[ques_model][asin] = []
                is_specific_scores[ques_model][asin] = []
                new_info_scores[ques_model][asin] = []
                customer_support_scores[ques_model][asin] = []
                useful_to_another_buyer_scores[ques_model][asin] = []
                asin_model.append((asin, ques_model))
            ques = row['ques']
            on_topic = row['on_topic']
            is_specific = row['is_specific']
            new_info = row['new_info']
            customer_support = row['customer_support']
            useful_to_another_buyer = row['useful_to_another_buyer']
            
            on_topic_scores[ques_model][asin].append(on_topic_levels[on_topic])
            is_specific_scores[ques_model][asin].append(is_specific_levels[is_specific])
            new_info_scores[ques_model][asin].append(new_info_levels[new_info])
            customer_support_scores[ques_model][asin].append(customer_support_levels[customer_support])
            useful_to_another_buyer_scores[ques_model][asin].append(useful_to_another_buyer_levels[useful_to_another_buyer])

    print len(on_topic_scores['lucene_new'].keys())
    print
    missing_asins = []
    for asin in on_topic_scores['lucene_new'].keys():
        missing = False
        for ques_model in model_names:
            if asin not in on_topic_scores[ques_model] or len(on_topic_scores[ques_model][asin]) < 3:
                missing = True
                break
        if missing:
            missing_asins.append(asin)
            continue
        for ques_model in model_names:
            on_topic_scores_list[ques_model] += on_topic_scores[ques_model][asin]
            is_specific_scores_list[ques_model] += is_specific_scores[ques_model][asin]
            new_info_scores_list[ques_model] += new_info_scores[ques_model][asin]
            customer_support_scores_list[ques_model] += customer_support_scores[ques_model][asin]
            useful_to_another_buyer_scores_list[ques_model] += useful_to_another_buyer_scores[ques_model][asin]
    print len(missing_asins)
    print
    #for asin in missing_asins:
    #    if asin in gold_asin_model:
    #        print asin, gold_asin_model[asin]
    for model in model_names:
        print model, len(on_topic_scores_list[model])
        print '%.3f' % np.mean(on_topic_scores_list[model]), \
                on_topic_scores_list[model].count(0), \
                on_topic_scores_list[model].count(1), \
                on_topic_scores_list[model].count(2), \
                on_topic_scores_list[model].count(3)
        print '%.3f' % np.mean(is_specific_scores_list[model]), \
                is_specific_scores_list[model].count(0), \
                is_specific_scores_list[model].count(1), \
                is_specific_scores_list[model].count(2), \
                is_specific_scores_list[model].count(3)
        print '%.3f' % np.mean(new_info_scores_list[model]), \
                new_info_scores_list[model].count(0), \
                new_info_scores_list[model].count(1), \
                new_info_scores_list[model].count(2)
        print '%.3f' % np.mean(customer_support_scores_list[model]), \
                customer_support_scores_list[model].count(0), \
                customer_support_scores_list[model].count(1)
        print '%.3f' % np.mean(useful_to_another_buyer_scores_list[model]), \
                useful_to_another_buyer_scores_list[model].count(0), \
                useful_to_another_buyer_scores_list[model].count(1), \
                useful_to_another_buyer_scores_list[model].count(2), \
                useful_to_another_buyer_scores_list[model].count(3)
        print
    
if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--full_results", type = str)
    argparser.add_argument("--full_results_v4", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)
