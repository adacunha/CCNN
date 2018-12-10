import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

class Player:

	def __init__(self, player):
		self.player = player

		# Setup neural networks
		self.load_policy_network()
		self.load_value_network()

	def load_policy_network(self):

		policy_network_name = "64c_32c_1000r"

		self.policy_network = tf.keras.models.Sequential([
			keras.layers.Conv2D(64, kernel_size=(2, 2), strides=(1, 1), activation='relu', input_shape=(8,4,1)),
			keras.layers.Conv2D(32, kernel_size=(2, 2), strides=(1, 1), activation='relu'),
			keras.layers.Flatten(),
			keras.layers.Dense(1024, activation='relu'),
			keras.layers.Dense(128, activation=tf.nn.softmax)
		])

		checkpoint_path = "policy_network_checkpoints/" + policy_network_name + ".ckpt"
		checkpoint_dir = os.path.dirname(checkpoint_path)
		latest_policy_network_weights = tf.train.latest_checkpoint(checkpoint_dir)
		self.policy_network.load_weights(latest_policy_network_weights)

	def load_value_network(self):

		value_network_name = "64c_32c_1000r"

		self.value_network = tf.keras.models.Sequential([
			keras.layers.Conv2D(64, kernel_size=(2, 2), strides=(1, 1), activation='relu', input_shape=(8,4,1)),
			keras.layers.Conv2D(32, kernel_size=(2, 2), strides=(1, 1), activation='relu'),
			keras.layers.Flatten(),
			keras.layers.Dense(1024, activation='relu'),
			keras.layers.Dense(3, activation=tf.nn.softmax)
		])

		checkpoint_path = "value_network_checkpoints/" + value_network_name + ".ckpt"
		checkpoint_dir = os.path.dirname(checkpoint_path)
		latest_value_network_weights = tf.train.latest_checkpoint(checkpoint_dir)
		self.value_network.load_weights(latest_value_network_weights)
		
	def evaluate_turn_policy(self, board):
		move_guess = self.policy_network.predict(np.array([board.get_cnn_input(self.player)]))[0]
		move_guess = board.clean_nn_guess(move_guess, self.player)
		return move_guess
	
	def evaluate_turn_value(self, board):
		outcome_guess = self.value_network.predict(np.array([board.get_cnn_input(self.player)]))[0]
		return outcome_guess

	def play_turn(self, board):
		best_move = self.mcts(board)

	class Node:
		def __init__(self, move, prior, board):
			self.move = move
			self.prior = prior
			self.visit_count = 0
			self.evaluation_sum = 0
			self.mixing_hyperparameter = .5
			self.board = board	
			self.children = set()	

		def get_exporation_score(self):
			return self.prior / (1 + self.visit_count)

		def get_exploitation_score(self):
			if self.visit_count == 0:
				return 0
			return self.evaluation_sum / self.visit_count	

		def get_node_score(self):
			return self.get_exploration_score() * mixing_hyperparamter + self.get_exploitation_score() * (1-mixing_hyperparameter)

		def is_expanded(self):
			return len(self.children) > 0

		def traverse_to_leaf(self):
			if not self.is_expanded():
				return self
			
	
	def mcts(self, board):
		start = Node(0, board)
