import argparse
import csv
import sys
import numpy as np
import pdb
from collections import defaultdict

def main(args):
    new_csvfile = open(args.new_aggregate_results, 'w')
    writer = csv.writer(new_csvfile, delimiter=',')
    writer.writerow(['_unit_id','_golden','_unit_state','_trusted_judgments','_last_judgment_at', \
                     'customer_support','customer_support:confidence','is_specific','is_specific:confidence', \
                     'new_info','new_info:confidence','on_topic','on_topic:confidence','useful_to_another_buyer','useful_to_another_buyer:confidence', \
                     'asin','customer_support_gold','description','is_specific_gold','new_info_gold','on_topic_gold','ques','ques_model','title','useful_to_another_buyer_gold'])
    with open(args.aggregate_results) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ques_model = row['ques_model']
            if ques_model == 'lucene':
                continue
            writer.writerow([row['_unit_id'], row['_golden'], row['_unit_state'], row['_trusted_judgments'], row['_last_judgment_at'], \
                            row['customer_support'], row['customer_support:confidence'], row['is_specific'], row['is_specific:confidence'], \
                            row['new_info'], row['new_info:confidence'], row['on_topic'], row['on_topic:confidence'], \
                            row['useful_to_another_buyer'], row['useful_to_another_buyer:confidence'], row['asin'], row['customer_support_gold'], \
                            row['description'], row['is_specific_gold'], row['new_info_gold'], row['on_topic_gold'], \
                            row['ques'], row['ques_model'], row['title'], row['useful_to_another_buyer_gold']])

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--aggregate_results", type = str)
    argparser.add_argument("--new_aggregate_results", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)
