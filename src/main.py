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

post_data_tsvfile = sys.argv[1]
qa_data_tsvfile = sys.argv[2]
lucene_sim_ques_file = sys.argv[3]
p_input_data, q_input_data, output_data, triples = prepare_data(post_data_tsvfile, qa_data_tsvfile, lucene_sim_ques_file)

N = int(len(triples)*0.8)
train_triples = triples[:N]
test_triples = triples[N:]

# Initialize models
encoder = EncoderRNN(input_data.n_words, hidden_size, n_layers, dropout=dropout)
decoder = AttnDecoderRNN(attn_model, hidden_size, output_data.n_words, n_layers)

# Initialize optimizers and criterion
encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate * decoder_learning_ratio)
criterion = nn.CrossEntropyLoss()

# Move models to GPU
if USE_CUDA:
	encoder.cuda()
	decoder.cuda()
	print 'Using CUDA'

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

print 'No. of triples %d' % len(triples)

while epoch < n_epochs:
	epoch += 1
	
	# Get training data for this cycle
	input_batches, input_lengths, target_batches, target_lengths = random_batch(batch_size, input_data, output_data, train_triples)

	# Run the train function
	#print 'Running training...'
	loss, ec, dc = train(
		input_batches, input_lengths, target_batches, target_lengths,
		encoder, decoder,
		encoder_optimizer, decoder_optimizer, criterion
	)
	#print 'Done'

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
		evaluate_randomly(input_data, output_data, test_triples, encoder, decoder)

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
