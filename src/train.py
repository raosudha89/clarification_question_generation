import torch
from torch.autograd import Variable
from masked_cross_entropy import *

from constants import *

def train(p_input_batches, p_input_lengths, q_input_batches, q_input_lengths, target_batches, target_lengths, \
			p_encoder, encoder, decoder, p_encoder_optimizer, encoder_optimizer, decoder_optimizer, criterion):
	
	# Zero gradients of both optimizers
	p_encoder_optimizer.zero_grad()
	encoder_optimizer.zero_grad()
	decoder_optimizer.zero_grad()
	loss = 0 # Added onto for each word

	# Run post words through p_encoder
	#p_encoder_output = p_encoder(p_input_batches)	
	p_encoder_outputs, p_encoder_hidden = p_encoder(p_input_batches, p_input_lengths, None)	

	# Run words through encoder
	encoder_outputs, encoder_hidden = encoder(q_input_batches, q_input_lengths, None)
	
	# Prepare input and output variables
	decoder_input = Variable(torch.LongTensor([SOS_token] * batch_size))
	#decoder_hidden = p_encoder_output + encoder_hidden[:decoder.n_layers] # Use avg p emb + last (forward) hidden state from encoder
	decoder_hidden = encoder_hidden[:decoder.n_layers] # Use last (forward) hidden state from encoder

	max_target_length = max(target_lengths)
	all_decoder_outputs = Variable(torch.zeros(max_target_length, batch_size, decoder.output_size))

	# Move new Variables to CUDA
	if USE_CUDA:
		decoder_input = decoder_input.cuda()
		all_decoder_outputs = all_decoder_outputs.cuda()

	# Run through decoder one time step at a time
	#print 'max target len %d ' % max_target_length
	for t in range(max_target_length):
		decoder_output, decoder_hidden, decoder_attn = decoder(
			decoder_input, decoder_hidden, p_encoder_outputs
		)

		all_decoder_outputs[t] = decoder_output
		decoder_input = target_batches[t] # Next input is current target

	# Loss calculation and backpropagation
	loss = masked_cross_entropy(
		all_decoder_outputs.transpose(0, 1).contiguous(), # -> batch x seq
		target_batches.transpose(0, 1).contiguous(), # -> batch x seq
		target_lengths
	)
	loss.backward()
	
	# Clip gradient norms
	ec = torch.nn.utils.clip_grad_norm(p_encoder.parameters(), clip)
	ec = torch.nn.utils.clip_grad_norm(encoder.parameters(), clip)
	dc = torch.nn.utils.clip_grad_norm(decoder.parameters(), clip)

	# Update parameters with optimizers
	p_encoder_optimizer.step()
	encoder_optimizer.step()
	decoder_optimizer.step()
	
	return loss.data[0], ec, dc
