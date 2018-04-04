import torch
from torch.autograd import Variable
from read_data import *
import random

from constants import *

MIN_LENGTH = 3
MAX_LENGTH = 25
def filter_pairs(pairs):
	filtered_pairs = []
	for pair in pairs:
		if len(pair[0]) >= MIN_LENGTH and len(pair[0]) <= MAX_LENGTH \
			and len(pair[1]) >= MIN_LENGTH and len(pair[1]) <= MAX_LENGTH:
				filtered_pairs.append(pair)
	return filtered_pairs

def trim_pairs(pairs):
	keep_pairs = []

	for pair in pairs:
		input_sentence = pair[0]
		output_sentence = pair[1]
		keep_input = True
		keep_output = True
	
		for word in input_sentence.split(' '):
			if word not in input_data.word2index:
				keep_input = False
				break

		for word in output_sentence.split(' '):
			if word not in output_data.word2index:
				keep_output = False
				break

		# Remove if pair doesn't match input and output conditions
		if keep_input and keep_output:
			keep_pairs.append(pair)

	print("Trimmed from %d pairs to %d, %.4f of total" % (len(pairs), len(keep_pairs), len(keep_pairs)*1.0 / len(pairs)))
	return keep_pairs	

def prepare_data(post_data_tsv, qa_data_tsv):
	input_data, output_data, pairs = read_data(post_data_tsv, qa_data_tsv)

	print("Indexing words...")
	for pair in pairs:
		input_data.index_words(pair[0])
		output_data.index_words(pair[1])
	
	print('Indexed %d words in input language, %d words in output' % (input_data.n_words, output_data.n_words))

	input_data.trim_using_tfidf()
	output_data.trim(MIN_COUNT)

	#pairs = trim_pairs(pairs)
	return input_data, output_data, pairs

# Return a list of indexes, one for each word in the sentence, plus EOS
def indexes_from_sentence(lang, sentence):
	indices = []
	for word in sentence.split(' '):
		if word in lang.word2index:
			indices.append(lang.word2index[word])
		#else:
		#	indices.append(UNK_token)
	indices.append(EOS_token)
	return indices
	#return [lang.word2index[word] for word in sentence.split(' ')] + [EOS_token]


# Pad a with the PAD symbol
def pad_seq(seq, max_length):
	seq += [PAD_token for i in range(max_length - len(seq))]
	return seq

def random_batch(batch_size, input_data, output_data, pairs):
	input_seqs = []
	target_seqs = []

	# Choose random pairs
	for i in range(batch_size):
		pair = random.choice(pairs)
		input_seqs.append(indexes_from_sentence(input_data, pair[0]))
		target_seqs.append(indexes_from_sentence(output_data, pair[1]))

	# Zip into pairs, sort by length (descending), unzip
	seq_pairs = sorted(zip(input_seqs, target_seqs), key=lambda p: len(p[0]), reverse=True)
	input_seqs, target_seqs = zip(*seq_pairs)
	
	# For input and target sequences, get array of lengths and pad with 0s to max length
	input_lengths = [len(s) for s in input_seqs]
	input_padded = [pad_seq(s, max(input_lengths)) for s in input_seqs]
	target_lengths = [len(s) for s in target_seqs]
	target_padded = [pad_seq(s, max(target_lengths)) for s in target_seqs]

	# Turn padded arrays into (batch_size x max_len) tensors, transpose into (max_len x batch_size)
	input_var = Variable(torch.LongTensor(input_padded)).transpose(0, 1)
	target_var = Variable(torch.LongTensor(target_padded)).transpose(0, 1)
	
	if USE_CUDA:
		input_var = input_var.cuda()
		target_var = target_var.cuda()
		
	return input_var, input_lengths, target_var, target_lengths
