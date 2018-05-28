import argparse
import csv
import sys
import numpy as np
from nltk.util import ngrams
import pdb

is_specific_levels = {'Strongly Agree': 3, 'Agree': 2, 'Disagree': 1, 'Strongly Disagree': 0, \
                      'Totalmente de acuerdo': 3}
asks_new_info_levels = {'Completely': 3, 'Partially': 2, 'Somewhat': 1, 'No': 0, \
                        'Completamente': 3, 'Parcialmente': 2}
is_grammatical_levels = {'Perfect': 3, 'Comprehensible': 2, 'Somewhat Comprehensible': 1, 'Incomprehensible': 0, \
                         'Perfecto': 3}
rank_levels = {'1 (best)': 1, '2': 2, '3': 3, '4': 4, '5': 4, \
               '1 (mejor)': 1}


model_names = {'gold': 0, 'lucene': 1, 'nocontext': 2, 'onlycontext':3, 'candqs': 4, 'candqs_template': 5}
model_list = ['gold', 'lucene', 'nocontext', 'onlycontext', 'candqs', 'candqs_template']

def main(args):
    is_specific = {}
    asks_new_info = {}
    is_grammatical = {}
    ranks = {}
    questions = {}
    with open(args.aggregate_results) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asin = row['asin']
            if asin not in questions:
                questions[asin] = [None]*6
                is_specific[asin] = [None]*6
                asks_new_info[asin] = [None]*6
                is_grammatical[asin] = [None]*6
                ranks[asin] = [None]*6
                for i in range(6):
                    is_specific[asin][i] = []
                    asks_new_info[asin][i] = []
                    is_grammatical[asin][i] = []
                    ranks[asin][i] = []
            
            models = [None]*5
            models[0] = row['q1_model']
            models[1] = row['q2_model']
            models[2] = row['q3_model']
            models[3] = row['q4_model']
            models[4] = row['q5_model']
            
            if questions[asin][model_names[models[0]]]:
                assert(questions[asin][model_names[models[0]]] == row['q1'])
            else:
                questions[asin][model_names[models[0]]] = row['q1']
            if questions[asin][model_names[models[1]]]:
                assert(questions[asin][model_names[models[1]]] == row['q2'])
            else:
                questions[asin][model_names[models[1]]] = row['q2']
            if questions[asin][model_names[models[2]]]:
                assert(questions[asin][model_names[models[2]]] == row['q3'])
            else:
                questions[asin][model_names[models[2]]] = row['q3']
            if questions[asin][model_names[models[3]]]:
                assert(questions[asin][model_names[models[3]]] == row['q4'])
            else:
                questions[asin][model_names[models[3]]] = row['q4']
            if questions[asin][model_names[models[4]]]:
                assert(questions[asin][model_names[models[4]]] == row['q5'])
            else:
                questions[asin][model_names[models[4]]] = row['q5']
            
            is_specific[asin][model_names[models[0]]].append(is_specific_levels[row['q1_is_specific']])
            is_specific[asin][model_names[models[1]]].append(is_specific_levels[row['q2_is_specific']])
            is_specific[asin][model_names[models[2]]].append(is_specific_levels[row['q3_is_specific']])
            is_specific[asin][model_names[models[3]]].append(is_specific_levels[row['q4_is_specific']])
            is_specific[asin][model_names[models[4]]].append(is_specific_levels[row['q5_is_specific']])
            
            asks_new_info[asin][model_names[models[0]]].append(asks_new_info_levels[row['q1_asks_for_new_information']])
            asks_new_info[asin][model_names[models[1]]].append(asks_new_info_levels[row['q2_asks_for_new_information']])
            asks_new_info[asin][model_names[models[2]]].append(asks_new_info_levels[row['q3_asks_for_new_information']])
            asks_new_info[asin][model_names[models[3]]].append(asks_new_info_levels[row['q4_asks_for_new_information']])
            asks_new_info[asin][model_names[models[4]]].append(asks_new_info_levels[row['q5_asks_for_new_information']])
            
            is_grammatical[asin][model_names[models[0]]].append(is_grammatical_levels[row['q1_is_grammatical']])
            is_grammatical[asin][model_names[models[1]]].append(is_grammatical_levels[row['q2_is_grammatical']])
            is_grammatical[asin][model_names[models[2]]].append(is_grammatical_levels[row['q3_is_grammatical']])
            is_grammatical[asin][model_names[models[3]]].append(is_grammatical_levels[row['q4_is_grammatical']])
            is_grammatical[asin][model_names[models[4]]].append(is_grammatical_levels[row['q5_is_grammatical']])
            
            ranks[asin][model_names[models[0]]].append(rank_levels[row['rank_of_q1']])
            ranks[asin][model_names[models[1]]].append(rank_levels[row['rank_of_q2']])
            ranks[asin][model_names[models[2]]].append(rank_levels[row['rank_of_q3']])
            ranks[asin][model_names[models[3]]].append(rank_levels[row['rank_of_q4']])
            ranks[asin][model_names[models[4]]].append(rank_levels[row['rank_of_q5']])
        
    is_specific_scores = [0.0]*6
    asks_new_info_scores = [0.0]*6
    is_grammatical_scores = [0.0]*6
    rank_scores = [0.0]*6
    questions_lens = [None]*6
    for i in range(6):
        is_specific_scores[i] = []
        asks_new_info_scores[i] = []
        is_grammatical_scores[i] = []
        rank_scores[i] = []
        questions_lens[i] = []
        
    for asin in ranks:
        for i in range(6):
            if questions[asin][i] == None:
                print asin, model_list[i]
            else:
                questions_lens[i].append(len(questions[asin][i]))
                is_specific_scores[i].append(np.mean(np.array(is_specific[asin][i])))
                asks_new_info_scores[i].append(np.mean(np.array(asks_new_info[asin][i])))
                is_grammatical_scores[i].append(np.mean(np.array(is_grammatical[asin][i])))
                rank_scores[i].append(np.mean(np.array(ranks[asin][i])))
    
    for i in range(6):
        print model_list[i]
        print '%.3f, %.3f' % (np.mean(np.array(is_specific_scores[i])), np.std(np.array(is_specific_scores[i])))
        print '%.3f, %.3f' % (np.mean(np.array(asks_new_info_scores[i])), np.std(np.array(asks_new_info_scores[i])))
        print '%.3f, %.3f' % (np.mean(np.array(is_grammatical_scores[i])), np.std(np.array(is_grammatical_scores[i])))
        print '%.3f, %.3f' % (np.mean(np.array(rank_scores[i])), np.std(np.array(rank_scores[i])))
        print 'Mean len %.3f' % (np.mean(np.array(questions_lens[i])))
        print 'Median len %.3f' % (np.median(np.array(questions_lens[i])))
        print


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--aggregate_results", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)