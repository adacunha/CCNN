import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import seaborn as sns

import TTT

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

	def get_move(self, board, player):
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
