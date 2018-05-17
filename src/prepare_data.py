import torch
from torch.autograd import Variable
from read_data import *
import random

from constants import *

def prepare_data(post_data_tsv, qa_data_tsv, train_ids_file, test_ids_file, sim_ques_filename):
	p_input_data, q_data, train_triples, test_triples = read_data(post_data_tsv, qa_data_tsv, train_ids_file, test_ids_file, sim_ques_filename)

	triples = train_triples + test_triples
	print("Indexing words...")
	for triple in triples:
		p_input_data.index_words(triple[0])
		for q in triple[1]:
			q_data.index_words(q)
		q_data.index_words(triple[2])
	
	print('Indexed %d words in post input, %d words in ques' % (p_input_data.n_words, q_data.n_words))

	p_input_data.trim_using_tfidf()
	q_data.trim(MIN_COUNT)

	return p_input_data, q_data, train_triples, test_triples

# Return a list of indexes, one for each word in the sentence, plus EOS
def indexes_from_sentence(lang, sentence):
	indices = []
	for word in sentence.split(' '):
		if word in lang.word2index:
			indices.append(lang.word2index[word])
	indices.append(EOS_token)
	return indices

# Pad a with the PAD symbol
def pad_seq(seq, max_length):
	seq += [PAD_token for i in range(max_length - len(seq))]
	return seq

def random_batch(batch_size, p_input_data, q_data, triples):
	p_input_seqs = []
	q_input_seqs = []
	target_seqs = []

	# Choose random triples
	for i in range(batch_size):
		triple = random.choice(triples)
		p_input_seqs.append(indexes_from_sentence(p_input_data, triple[0]))
		ques_list = []
		for ques in triple[1]:
			ques_list.append(indexes_from_sentence(q_data, ques))
		q_input_seqs.append(ques_list)
		target_seqs.append(indexes_from_sentence(q_data, triple[2]))

	# Zip into triples, sort by length (descending), unzip
	seq_triples = sorted(zip(p_input_seqs, q_input_seqs, target_seqs), key=lambda p: len(p[0]), reverse=True)
	p_input_seqs, q_input_seqs, target_seqs = zip(*seq_triples)
	
	# For input and target sequences, get array of lengths and pad with 0s to max length
	p_input_lengths = [len(s) for s in p_input_seqs]
	p_input_padded = [pad_seq(s, max(p_input_lengths)) for s in p_input_seqs]
	q_input_lengths_list = []
	q_input_padded_list = []
	max_len = 0
	for s_list in q_input_seqs:
		q_input_lengths_list.append([len(s) for s in s_list])
		max_len = max(max_len, len(s))
	max_len += 1
	for s_list in q_input_seqs:
		q_input_padded_list.append([pad_seq(s, max_len) for s in s_list])
	target_lengths = [len(s) for s in target_seqs]
	target_padded = [pad_seq(s, max(target_lengths)) for s in target_seqs]

	# Turn padded arrays into (batch_size x max_len) tensors, transpose into (max_len x batch_size)
	p_input_var = Variable(torch.LongTensor(p_input_padded)).transpose(0, 1)
	q_input_var_list = []
	for q_input_padded in q_input_padded_list:
		q_input_var_list.append(Variable(torch.LongTensor(q_input_padded)).transpose(0, 1))
	target_var = Variable(torch.LongTensor(target_padded)).transpose(0, 1)
	
	if USE_CUDA:
		p_input_var = p_input_var.cuda()
		for i in range(len(q_input_var_list)):
			q_input_var_list[i] = q_input_var_list[i].cuda()
		target_var = target_var.cuda()
		
	return p_input_var, p_input_lengths, q_input_var_list, q_input_lengths_list, target_var, target_lengths
