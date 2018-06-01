import argparse
import csv
import sys
import numpy as np
from nltk.util import ngrams
import pdb
from collections import defaultdict

model_names = ['gold', 'lucene_new', 'simcandqs']
model_scores = {'gold':[], 'lucene_new':[], 'simcandqs':[]}

on_topic_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}}
is_specific_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}}
new_info_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}}
customer_support_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}}
useful_to_another_buyer_scores = {'gold':{}, 'lucene_new':{}, 'simcandqs':{}}

on_topic_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[]}
is_specific_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[]}
new_info_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[]}
customer_support_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[]}
useful_to_another_buyer_scores_list = {'gold':[], 'lucene_new':[], 'simcandqs':[]}

on_topic_levels = {'Strongly Agree': 3, 'Agree': 2, 'Disagree': 1, 'Strongly Disagree': 0}
is_specific_levels = {'Strongly Agree': 3, 'Agree': 2, 'Disagree': 1, 'Strongly Disagree': 0}
new_info_levels = {'Completely': 2, 'Somewhat': 1, 'No': 0}
customer_support_levels = {'Yes': 1, 'No': 0}
useful_to_another_buyer_levels = {'Strongly Agree': 3, 'Agree': 2, 'Disagree': 1, 'Strongly Disagree': 0}

def main(args):
    questions = {'gold': {}, 'lucene_new': {}, 'simcandqs': {}}
    asin_model = []
    with open(args.aggregate_results) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asin = row['asin']
            ques_model = row['ques_model']
            if ques_model not in model_names:
                continue
            #if (asin, ques_model) not in asin_model:
            #    asin_model.append((asin, ques_model))
            #else:
            #    continue
            ques = row['ques']
            on_topic = row['on_topic']
            is_specific = row['is_specific']
            new_info = row['new_info']
            customer_support = row['customer_support']
            useful_to_another_buyer = row['useful_to_another_buyer']
            
            on_topic_scores[ques_model][asin] = on_topic_levels[on_topic]
            is_specific_scores[ques_model][asin] = is_specific_levels[is_specific]
            new_info_scores[ques_model][asin] = new_info_levels[new_info]
            customer_support_scores[ques_model][asin] = customer_support_levels[customer_support]
            useful_to_another_buyer_scores[ques_model][asin] = useful_to_another_buyer_levels[useful_to_another_buyer]

    with open(args.aggregate_results_v4) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asin = row['asin']
            ques_model = row['ques_model']
            if ques_model != 'lucene_new':
                continue
            #if (asin, ques_model) not in asin_model:
            #    asin_model.append((asin, ques_model))
            #else:
            #    continue
            ques = row['ques']
            on_topic = row['on_topic']
            is_specific = row['is_specific']
            new_info = row['new_info']
            customer_support = row['customer_support']
            useful_to_another_buyer = row['useful_to_another_buyer']
            
            on_topic_scores[ques_model][asin] = on_topic_levels[on_topic]
            is_specific_scores[ques_model][asin] = is_specific_levels[is_specific]
            new_info_scores[ques_model][asin] = new_info_levels[new_info]
            customer_support_scores[ques_model][asin] = customer_support_levels[customer_support]
            useful_to_another_buyer_scores[ques_model][asin] = useful_to_another_buyer_levels[useful_to_another_buyer]

    for asin in on_topic_scores['lucene_new'].keys():
        for ques_model in model_names:
            on_topic_scores_list[ques_model].append(on_topic_scores[ques_model][asin])
            is_specific_scores_list[ques_model].append(is_specific_scores[ques_model][asin])
            new_info_scores_list[ques_model].append(new_info_scores[ques_model][asin])
            customer_support_scores_list[ques_model].append(customer_support_scores[ques_model][asin])
            useful_to_another_buyer_scores_list[ques_model].append(useful_to_another_buyer_scores[ques_model][asin])

    for model in model_names:
        print model, len(on_topic_scores_list[model])
        print np.mean(on_topic_scores_list[model]), \
                on_topic_scores_list[model].count(0), \
                on_topic_scores_list[model].count(1), \
                on_topic_scores_list[model].count(2), \
                on_topic_scores_list[model].count(3)
        print np.mean(is_specific_scores_list[model]), \
                is_specific_scores_list[model].count(0), \
                is_specific_scores_list[model].count(1), \
                is_specific_scores_list[model].count(2), \
                is_specific_scores_list[model].count(3)
        print np.mean(new_info_scores_list[model])
        print np.mean(customer_support_scores_list[model])
        print np.mean(useful_to_another_buyer_scores_list[model])
        print
    
if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--aggregate_results", type = str)
    argparser.add_argument("--aggregate_results_v4", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)
