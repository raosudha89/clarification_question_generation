import argparse
import string
import random
import time
import datetime
import math
import sys

import torch
import torch.nn as nn
from torch.autograd import Variable
from torch import optim
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence#, masked_cross_entropy
from masked_cross_entropy import *

import numpy as np

from prepare_data import *
from encoderRNN import *
from encoderAvgEmb import *
from attnDecoderRNN import *
from helper import *
from attn import *
from read_data import *
from train import *
from evaluate import *
from visualize import * 
import socket
hostname = socket.gethostname()

from constants import *

def load_pretrained_emb(word_vec_fname, p_data):
	pretrained_emb = np.random.rand(p_data.n_words, word_emb_size)
	word_vec_file = open(word_vec_fname, 'r')
	for line in word_vec_file.readlines():
		vals = line.rstrip().split(' ')
		word = vals[0]
		if word in p_data.word2index:
			pretrained_emb[p_data.word2index[word]] = map(float, vals[1:])
	return pretrained_emb

def main(args):

	p_data, q_data, triples = prepare_data(args.post_data_tsvfile, args.qa_data_tsvfile, args.sim_ques_fname)

	pretrained_emb = load_pretrained_emb(args.word_vec_fname, p_data)

	N = int(len(triples)*0.8)
	train_triples = triples[:N]
	test_triples = triples[N:]

	# Initialize models
	avg_emb_encoder = EncoderAvgEmb(pretrained_emb)
	encoder = EncoderRNN(q_data.n_words, hidden_size, n_layers, dropout=dropout)
	decoder = AttnDecoderRNN(attn_model, hidden_size, q_data.n_words, n_layers)

	# Initialize optimizers and criterion
	encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
	decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate * decoder_learning_ratio)
	criterion = nn.CrossEntropyLoss()

	# Move models to GPU
	if USE_CUDA:
		avg_emb_encoder.cuda()
		encoder.cuda()
		decoder.cuda()

	import sconce
	job = sconce.Job('seq2seq-translate', {
		'attn_model': attn_model,
		'n_layers': n_layers,
		'dropout': dropout,
		'hidden_size': hidden_size,
		'learning_rate': learning_rate,
		'clip': clip,
		'teacher_forcing_ratio': teacher_forcing_ratio,
		'decoder_learning_ratio': decoder_learning_ratio,
	})
	job.plot_every = plot_every
	job.log_every = print_every

	# Keep track of time elapsed and running averages
	start = time.time()
	plot_losses = []
	print_loss_total = 0 # Reset every print_every
	plot_loss_total = 0 # Reset every plot_every

	ecs = []
	dcs = []
	eca = 0
	dca = 0
	epoch = 0.0
	
	print 'No. of triples %d' % len(triples)
	
	while epoch < n_epochs:
		epoch += 1
		
		# Get training data for this cycle
		p_input_batches, p_input_lengths, q_input_batches, q_input_lengths, target_batches, target_lengths = \
								random_batch(batch_size, p_data, q_data, train_triples)
	
		# Run the train function
		loss, ec, dc = train(
			p_input_batches, p_input_lengths, 
			q_input_batches, q_input_lengths, 
			target_batches, target_lengths,
			avg_emb_encoder, encoder, decoder,
			encoder_optimizer, decoder_optimizer, criterion
		)
	
		# Keep track of loss
		print_loss_total += loss
		plot_loss_total += loss
		eca += ec
		dca += dc
		
		job.record(epoch, loss)

		if epoch % print_every == 0:
			print_loss_avg = print_loss_total / print_every
			print_loss_total = 0
			print_summary = '%s (%d %d%%) %.4f' % (time_since(start, epoch / n_epochs), epoch, epoch / n_epochs * 100, print_loss_avg)
			print(print_summary)
			
		if epoch % evaluate_every == 0:
			evaluate_randomly(p_data, q_data, test_triples, avg_emb_encoder, encoder, decoder)
	
		if epoch % plot_every == 0:
			plot_loss_avg = plot_loss_total / plot_every
			plot_losses.append(plot_loss_avg)
			plot_loss_total = 0
			
			# TODO: Running average helper
			ecs.append(eca / plot_every)
			dcs.append(dca / plot_every)
			ecs_win = 'encoder grad (%s)' % hostname
			dcs_win = 'decoder grad (%s)' % hostname
			#vis.line(np.array(ecs), win=ecs_win, opts={'title': ecs_win})
			#vis.line(np.array(dcs), win=dcs_win, opts={'title': dcs_win})
			eca = 0
			dca = 0


if __name__ == "__main__":
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--post_data_tsvfile", type = str)
	argparser.add_argument("--qa_data_tsvfile", type = str)
	argparser.add_argument("--sim_ques_fname", type = str)
	argparser.add_argument("--word_vec_fname", type = str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)
	
