import torch
import torch.nn as nn
from attn import *
from constants import *

class AttnDecoderRNN(nn.Module):
	def __init__(self, attn_model, hidden_size, output_size, n_layers=1, dropout=0.1):
		super(AttnDecoderRNN, self).__init__()

		# Keep for reference
		self.attn_model = attn_model
		self.hidden_size = hidden_size
		self.output_size = output_size
		self.n_layers = n_layers
		self.dropout = dropout

		# Define layers
		self.embedding = nn.Embedding(output_size, hidden_size)
		self.embedding_dropout = nn.Dropout(dropout)
		self.gru = nn.GRU(hidden_size, hidden_size, n_layers, dropout=dropout)
		self.concat = nn.Linear(hidden_size * 3, hidden_size)
		self.out = nn.Linear(hidden_size, output_size)
		
		# Choose attention model
		if attn_model != 'none':
			self.attn = Attn(attn_model, hidden_size)

	def forward(self, input_seq, last_hidden, p_encoder_outputs, q_encoder_outputs):
		# Note: we run this one step at a time

		# Get the embedding of the current input word (last output word)
		batch_size = input_seq.size(0)
		embedded = self.embedding(input_seq)
		embedded = self.embedding_dropout(embedded)
		embedded = embedded.view(1, batch_size, self.hidden_size) # S=1 x B x N

		# Get current hidden state from input word and last hidden state
		rnn_output, hidden = self.gru(embedded, last_hidden)

		# Calculate attention from current RNN state and all p_encoder outputs;
		# apply to p_encoder outputs to get weighted average
		p_attn_weights = self.attn(rnn_output, p_encoder_outputs)
		p_context = p_attn_weights.bmm(p_encoder_outputs.transpose(0, 1)) # B x S=1 x N

		# Calculate attention from current RNN state and all q_encoder outputs;
		# apply to q_encoder outputs to get weighted average
		q_attn_weights = self.attn(rnn_output, q_encoder_outputs)
		q_context = q_attn_weights.bmm(q_encoder_outputs.transpose(0, 1)) # B x S=1 x N

		# Attentional vector using the RNN hidden state and context vector
		# concatenated together (Luong eq. 5)
		rnn_output = rnn_output.squeeze(0) # S=1 x B x N -> B x N

		p_context = p_context.squeeze(1)	   # B x S=1 x N -> B x N
		q_context = q_context.squeeze(1)	   # B x S=1 x N -> B x N
		concat_input = torch.cat((rnn_output, p_context, q_context), 1)
		concat_output = F.tanh(self.concat(concat_input))

		# Finally predict next token (Luong eq. 6, without softmax)
		output = self.out(concat_output)

		# Return final output, hidden state, and attention weights (for visualization)
		return output, hidden, p_attn_weights, q_attn_weights
