import sys
import argparse
import os

def main(args):
	prods = {}
	ques = {}
	for fname in os.listdir(args.prod_dir):
		

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--prod_dir", type = str)
	argparser.add_argument("--ques_dir", type = str)
	argparser.add_argument("--lucene_sim_prod", type = str)
	argparser.add_argument("--lucene_sim_ques", type = str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)


