import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import seaborn as sns

import TTT
import Node

class Alpha:

	def __init__(self, policy_nn_size, policy_nn_file, value_nn_size, value_nn_file):

		self.policy_model = tf.keras.models.Sequential([
			layers.Dense(policy_nn_size, activation=tf.nn.relu),
			layers.Dense(9, activation=tf.nn.softmax)
		])
		self.policy_model.load_weights(tf.train.latest_checkpoint(os.path.dirname(policy_nn_file)))

		self.value_model = tf.keras.models.Sequential([
			layers.Dense(value_nn_size, activation=tf.nn.relu),
			layers.Dense(1)
		])
		self.value_model.load_weights(tf.train.latest_checkpoint(os.path.dirname(value_nn_file)))

	def get_policy_move(self, board, player):
		policy_guess = (self.policy_model.predict(np.array([board.get_nn_input(player)])))[0]
		tot_prob = 0
		for i, v in enumerate(policy_guess):
			row = int(i / 3)
			col = i % 3
			if(not board.is_valid_move(row, col)):
				policy_guess[i] = 0
			else:
				tot_prob += policy_guess[i]
		max_guess = -1
		max_index = -1
		for i, v in enumerate(policy_guess):
			if(v > max_guess):
				max_guess = v #/total_prob
				max_index = i	
		return (int(max_index/3), max_index%3)

	def rollout(self, board, player):
		if(board.has_won()):
			return board.has_won();
		if(board.drawn()):
			return 0
		move = self.get_policy_move(board, player)
		board.place_piece(move[0], move[1], player)
		return self.rollout(board, player*-1)
			
	# Use the networks to do MCTS
	def get_move(self, board, player):
		root = Node.Node((-1, -1), 1)
		for i in range (0, 1000):
			t_board = board.get_copy()
			history = set()
			leaf = root.traverse(t_board, player, history)
			leaf_node = leaf[0]
			leaf_player = leaf[1]
			leaf_node.expand(t_board, leaf_player, self)
			leaf_value = (self.value_model.predict(np.array([t_board.get_nn_input(player)])))[0]
			rollout_result = self.rollout(t_board, leaf_player)	
			tot_score = .25 * rollout_result + .75 * leaf_value
			for node in history:
				node.value += tot_score
		max_count = -1
		max_n = None
		for move_node in root.children:
			if(move_node.visit_count > max_count):
				max_count = move_node.visit_count
				max_n = move_node	
		return max_n.coord
