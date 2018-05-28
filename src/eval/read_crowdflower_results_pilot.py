import argparse
import csv
import sys
import numpy as np
from nltk.util import ngrams
import pdb

on_topic_levels = {'Completely': 3, 'Partially': 2, 'Somewhat': 1, 'No': 0}
asks_new_info_levels = {'Completely': 3, 'Partially': 2, 'Somewhat': 1, 'No': 0}
is_grammatical_levels = {'Perfect': 3, 'Comprehensible': 2, 'Somewhat Comprehensible': 1, 'Incomprehensible': 0}
rank_levels = {'1 (best)': 1, '2': 2, '3': 3, '4': 4}

model_names = {'gold': 0, 'onlycontext':1, 'simcandqs': 2, 'simcandqs_template': 3}
model_list = ['gold', 'onlycontext', 'simcandqs', 'simcandqs_template']

def main(args):
    on_topic = {}
    asks_new_info = {}
    is_grammatical = {}
    ranks = {}
    questions = {}
    with open(args.aggregate_results) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asin = row['asin']
            questions[asin] = [None]*4
            on_topic[asin] = [None]*4
            asks_new_info[asin] = [None]*4
            is_grammatical[asin] = [None]*4
            ranks[asin] = [None]*4
            
            models = [None]*4
            models[0] = row['q1_model']
            models[1] = row['q2_model']
            models[2] = row['q3_model']
            models[3] = row['q4_model']
            
            questions[asin][model_names[models[0]]] = row['q1']
            questions[asin][model_names[models[1]]] = row['q2']
            questions[asin][model_names[models[2]]] = row['q3']
            questions[asin][model_names[models[3]]] = row['q4']
            
            on_topic[asin][model_names[models[0]]] = on_topic_levels[row['q1_is_on_topic']]
            on_topic[asin][model_names[models[1]]] = on_topic_levels[row['q2_is_on_topic']]
            on_topic[asin][model_names[models[2]]] = on_topic_levels[row['q3_is_on_topic']]
            on_topic[asin][model_names[models[3]]] = on_topic_levels[row['q4_is_on_topic']]
            
            asks_new_info[asin][model_names[models[0]]] = asks_new_info_levels[row['q1_asks_for_new_information']]
            asks_new_info[asin][model_names[models[1]]] = asks_new_info_levels[row['q2_asks_for_new_information']]
            asks_new_info[asin][model_names[models[2]]] = asks_new_info_levels[row['q3_asks_for_new_information']]
            asks_new_info[asin][model_names[models[3]]] = asks_new_info_levels[row['q4_asks_for_new_information']]
            
            is_grammatical[asin][model_names[models[0]]] = is_grammatical_levels[row['q1_is_grammatical']]
            is_grammatical[asin][model_names[models[1]]] = is_grammatical_levels[row['q2_is_grammatical']]
            is_grammatical[asin][model_names[models[2]]] = is_grammatical_levels[row['q3_is_grammatical']]
            is_grammatical[asin][model_names[models[3]]] = is_grammatical_levels[row['q4_is_grammatical']]
            
            ranks[asin][model_names[models[0]]] = rank_levels[row['rank_of_q1']]
            ranks[asin][model_names[models[1]]] = rank_levels[row['rank_of_q2']]
            ranks[asin][model_names[models[2]]] = rank_levels[row['rank_of_q3']]
            ranks[asin][model_names[models[3]]] = rank_levels[row['rank_of_q4']]
        
    on_topic_scores = [0.0]*4
    asks_new_info_scores = [0.0]*4
    is_grammatical_scores = [0.0]*4
    rank_scores = [0.0]*4
    questions_lens = [None]*4
    uni_grams = [None]*4
    bi_grams = [None]*4
    tri_grams = [None]*4
    four_grams = [None]*4
    for i in range(4):
        questions_lens[i] = []
        uni_grams[i] = []
        bi_grams[i] = []
        tri_grams[i] = []
        four_grams[i] = []
        
    for asin in ranks:
        for i in range(4):
            on_topic_scores[i] += on_topic[asin][i]
            asks_new_info_scores[i] += asks_new_info[asin][i]
            is_grammatical_scores[i] += is_grammatical[asin][i]
            rank_scores[i] += ranks[asin][i]
            questions_lens[i].append(len(questions[asin][i].split()))
            uni_grams[i] += questions[asin][i].split()
            bi_grams[i] += [g for g in ngrams(questions[asin][i].split(), 2)]
            tri_grams[i] += [g for g in ngrams(questions[asin][i].split(), 3)]
            four_grams[i] += [g for g in ngrams(questions[asin][i].split(), 4)]

    for i in range(4):
        print model_list[i]
        print '%.3f' % (on_topic_scores[i]/len(ranks))
        print '%.3f' % (asks_new_info_scores[i]/len(ranks))
        print '%.3f' % (is_grammatical_scores[i]/len(ranks))
        print '%.3f' % (rank_scores[i]/len(ranks))
        print 'Mean len %.3f' % (np.mean(np.array(questions_lens[i])))
        print 'Median len %.3f' % (np.median(np.array(questions_lens[i])))
        print 'Unique 1-gram %.3f' % (len(set(uni_grams[i]))/len(ranks))
        print 'Unique 2-gram %.3f' % (len(set(bi_grams[i]))/len(ranks))
        print 'Unique 3-gram %.3f' % (len(set(tri_grams[i]))/len(ranks))
        print 'Unique 4-gram %.3f' % (len(set(four_grams[i]))/len(ranks))
        
        print 'Unique 1-gram %.3f' % len(set(uni_grams[i]))
        print 'Unique 2-gram %.3f' % len(set(bi_grams[i]))
        print 'Unique 3-gram %.3f' % len(set(tri_grams[i]))
        print 'Unique 4-gram %.3f' % len(set(four_grams[i]))
        
        print 'Raw counts 1-gram %.3f' % len((uni_grams[i]))
        print 'Raw counts 2-gram %.3f' % len((bi_grams[i]))
        print 'Raw counts 3-gram %.3f' % len((tri_grams[i]))
        print 'Raw counts 4-gram %.3f' % len((four_grams[i]))

        print


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--aggregate_results", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)