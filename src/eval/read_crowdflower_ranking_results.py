import argparse
import csv
import sys
import numpy as np
from nltk.util import ngrams
import pdb
from scipy.stats import rankdata

model_names = ['gold', 'lucene', 'context', 'simcandqs', 'simcandqs_template']
model_scores = {'gold':[], 'lucene':[], 'context':[], 'simcandqs':[], 'simcandqs_template':[]}

score_dict = {'1 (best)': 1, '2': 2, '3': 3, '4': 4, '5': 5}

def main(args):
    irv_file = open(args.irv_format_file, 'w')
    irv_file.write('\t'.join(model_names)+'\n')
    with open(args.aggregate_ranking) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asin = row['asin']
            if row['q1_rank_gold'] != '':
                continue
            ranks = rankdata([score_dict[row['q1_rank']], \
                                score_dict[row['q2_rank']], \
                                score_dict[row['q3_rank']], \
                                score_dict[row['q4_rank']], \
                                score_dict[row['q5_rank']]], method='dense')
            org_ranks = [score_dict[row['q1_rank']], \
                                score_dict[row['q2_rank']], \
                                score_dict[row['q3_rank']], \
                                score_dict[row['q4_rank']], \
                                score_dict[row['q5_rank']]]
            for i in range(5):
                model_scores[row['q%d_model' % (i+1)]].append(ranks[i])
            irv_file.write('\t'.join([str(r) for r in org_ranks])+'\n')
    irv_file.close()
    for i in range(5):
        print model_names[i]
        print '%.3f' % np.mean(model_scores[model_names[i]]), len(model_scores[model_names[i]])
        print model_scores[model_names[i]].count(1), \
                model_scores[model_names[i]].count(2), \
                model_scores[model_names[i]].count(3), \
                model_scores[model_names[i]].count(4), \
                model_scores[model_names[i]].count(5)
        print

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--aggregate_ranking", type = str)
    argparser.add_argument("--irv_format_file", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)
