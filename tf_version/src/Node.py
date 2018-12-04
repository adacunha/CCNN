import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import seaborn as sns

class Node:
	def __init__(self, coord, prior):
		self.coord = coord
		self.children = set();
		self.prior = prior
		self.value = 0;
		self.visit_count = 0

	def get_exploitation_score(self):
		return self.prior / (1 + self.visit_count)
	def get_exploration_score(self):
		if(self.visit_count == 0):
			return 0
		return self.value / self.visit_count
	def get_score(self):
		return self.get_exploration_score() + self.get_exploitation_score()

	def traverse(self, board, player, history):
		self.visit_count += 1
		if(board.has_won() or board.drawn()):
			return (self, player)
		if(len(self.children) == 0):
			return (self, player);
		max_score = -1
		max_n = None
		for n in self.children:
			if(n.get_score() > max_score):
				max_score = n.get_score()
				max_n = n
		board.place_piece(max_n.coord[0], max_n.coord[1], player)
		return max_n.traverse(board, player * -1, history)

	def expand(self, board, player, alpha):
		self.visit_count += 1
		if(board.has_won() or board.drawn()):
			return
		priors = (alpha.policy_model.predict(np.array([board.get_nn_input(player)])))[0]
		tot_prob = 0
		for i, v in enumerate(priors):
			row = int(i / 3)
			col = i % 3
			if(not board.is_valid_move(row, col)):
				priors[i] = 0
			else:
				tot_prob += priors[i]
		for i, v in enumerate(priors):
			row = int(i / 3)
			col = i % 3
			n = Node((row, col), priors[i]/tot_prob)
			self.children.add(n)
