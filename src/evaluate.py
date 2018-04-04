import random
from constants import *
from prepare_data import indexes_from_sentence
import torch
import torch.nn as nn
from torch.autograd import Variable
from visualize import *

def evaluate_randomly(p_input_data, q_data, triples, avg_emb_encoder, encoder, decoder):
	[p_input_sentence, q_input_sentence, target_sentence] = random.choice(triples)
	evaluate_and_show_attention(p_input_data, q_data, avg_emb_encoder, encoder, decoder, p_input_sentence, q_input_sentence, target_sentence)
	
def evaluate_and_show_attention(p_input_data, q_data, avg_emb_encoder, encoder, decoder, p_input_sentence, q_input_sentence, target_sentence=None):
	output_words, attentions = evaluate(p_input_data, q_data, avg_emb_encoder, encoder, decoder, p_input_sentence, q_input_sentence)
	output_sentence = ' '.join(output_words)
	print('>', p_input_sentence)
	print('>', q_input_sentence)
	if target_sentence is not None:
		print('=', target_sentence)
	print('<', output_sentence)
	
	#show_attention(input_sentence, output_words, attentions)
	
	# Show input, target, output text in visdom
	#win = 'evaluted (%s)' % hostname
	#text = '<p>&gt; %s</p><p>= %s</p><p>&lt; %s</p>' % (input_sentence, target_sentence, output_sentence)
	#vis.text(text, win=win, opts={'title': win})

def evaluate(p_input_data, q_data, avg_emb_encoder, encoder, decoder, p_input_seq, q_input_seq, max_length=MAX_POST_LEN):
	p_input_seqs = [indexes_from_sentence(p_input_data, p_input_seq)]
	p_input_lengths = [len(p_input_seqs[0])]
	p_input_batches = Variable(torch.LongTensor(p_input_seqs), volatile=True).transpose(0, 1)
	
	q_input_seqs = [indexes_from_sentence(q_data, q_input_seq)]
	q_input_lengths = [len(q_input_seqs[0])]
	q_input_batches = Variable(torch.LongTensor(q_input_seqs), volatile=True).transpose(0, 1)
	
	if USE_CUDA:
		p_input_batches = p_input_batches.cuda()
		q_input_batches = q_input_batches.cuda()
		
	# Set to not-training mode to disable dropout
	encoder.train(False)
	decoder.train(False)
	
	# Run post words through avg_emb_encoder
	p_encoder_output = avg_emb_encoder(p_input_batches)	

	# Run through encoder
	encoder_outputs, encoder_hidden = encoder(q_input_batches, q_input_lengths, None)

	# Create starting vectors for decoder
	decoder_input = Variable(torch.LongTensor([SOS_token]), volatile=True) # SOS
	decoder_hidden = p_encoder_output + encoder_hidden[:decoder.n_layers] # Use last (forward) hidden state from encoder
	
	if USE_CUDA:
		decoder_input = decoder_input.cuda()

	# Store output words and attention states
	decoded_words = []
	decoder_attentions = torch.zeros(max_length + 1, max_length + 1)
	
	# Run through decoder
	for di in range(max_length):
		decoder_output, decoder_hidden, decoder_attention = decoder(
			decoder_input, decoder_hidden, encoder_outputs
		)
		decoder_attentions[di,:decoder_attention.size(2)] += decoder_attention.squeeze(0).squeeze(0).cpu().data

		# Choose top word from output
		topv, topi = decoder_output.data.topk(1)
		ni = topi[0][0]
		if ni == EOS_token:
			decoded_words.append('<EOS>')
			break
		else:
			decoded_words.append(q_data.index2word[ni])
			
		# Next input is chosen word
		decoder_input = Variable(torch.LongTensor([ni]))
		if USE_CUDA: decoder_input = decoder_input.cuda()

	# Set back to training mode
	encoder.train(True)
	decoder.train(True)
	
	return decoded_words, decoder_attentions[:di+1, :len(encoder_outputs)]
