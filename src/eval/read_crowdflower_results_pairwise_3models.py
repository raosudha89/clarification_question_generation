import argparse
import csv
import sys
import numpy as np
from nltk.util import ngrams
import pdb

model_names = ['gold', 'lucene', 'simcandqs']
model_scores = {'gold':[], 'lucene':[], 'simcandqs':[]}

def main(args):
    old_gold_qs = 0
    questions = {'gold': {}, 'lucene': {}, 'simcandqs': {}}
    model_pairs = {'gold_lucene': [0,0,0], 'gold_simcandqs': [0,0,0], 'lucene_simcandqs': [0,0,0]}
    q1_q2_asin = []
    with open(args.aggregate_results) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #if row['_golden'] == 'true':
            if row['answer_gold'] == '':
                continue
            asin = row['asin']
            q1_model = row['q1_model']
            q1 = row['q1']
            q2_model = row['q2_model']
            q2 = row['q2']
            if (q1_model, q2_model, asin)  not in q1_q2_asin:
                q1_q2_asin.append((q1_model, q2_model, asin))
            else:
                continue
            #if q1_model not in model_names or q2_model not in model_names:
             #   old_gold_qs += 1
              #  continue
            if q1_model+'_'+q2_model in model_pairs:
                if row['answer_gold'] == 'Q1 is more useful':
                    model_pairs[q1_model+'_'+q2_model][0] += 1
                elif row['answer_gold'] == 'Q2 is more useful':
                    model_pairs[q1_model+'_'+q2_model][1] += 1
                else:
                    model_pairs[q1_model+'_'+q2_model][2] += 1
            elif q2_model+'_'+q1_model in model_pairs:
                if row['answer_gold'] == 'Q1 is more useful':
                    model_pairs[q2_model+'_'+q1_model][1] += 1
                elif row['answer_gold'] == 'Q2 is more useful':
                    model_pairs[q2_model+'_'+q1_model][0] += 1
                else:
                    model_pairs[q2_model+'_'+q1_model][2] += 1
            questions[q1_model][asin] = q1
            questions[q2_model][asin] = q2
            #print '%s\t%s' % (q1_model, q2_model)
            #print '"%s"\t"%s"' % (q1, q2)
            #print row['answer_gold']
            #print
            if row['answer_gold'] == 'Q1 is more useful':
                model_scores[q1_model].append(1)
                model_scores[q2_model].append(-1)
            elif row['answer_gold'] == 'Q2 is more useful':
                model_scores[q2_model].append(1)
                model_scores[q1_model].append(-1)
            else:
                model_scores[q2_model].append(1)
                model_scores[q1_model].append(1)
    #print old_gold_qs
    for i in range(3):
        print model_names[i]
        print np.mean(model_scores[model_names[i]]), len(model_scores[model_names[i]])
        #print model_scores[model_names[i]]
        print
    for pair in model_pairs:
        print pair
        print model_pairs[pair]
        print 
    #gold_qfile = open('gold_questions.txt', 'w')
    #lucene_qfile = open('lucene_questions.txt', 'w')
    #simcandqs_qfile = open('simcandqs_questions.txt', 'w')
    #for asin in questions['gold']:
    #    gold_qfile.write(questions['gold'][asin]+'\n')
    #    lucene_qfile.write(questions['lucene'][asin]+'\n')
    #    simcandqs_qfile.write(questions['simcandqs'][asin]+'\n')

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--aggregate_results", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)