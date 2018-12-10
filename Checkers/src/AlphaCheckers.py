import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

import Checkers
from MCTS import Node 

class Player:

	def __init__(self):

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
		
	def evaluate_turn_policy(self, board, player):
		move_guess = self.policy_network.predict(np.array([board.get_cnn_input(player)]))[0]
		move_guess = board.clean_nn_guess(move_guess, player)
		return move_guess
	
	def evaluate_turn_value(self, board, player):
		outcome_guess = self.value_network.predict(np.array([board.get_cnn_input(player)]))[0]
		return outcome_guess

	def play_turn(self, board, player):
		best_move = self.mcts(board, player, 10)
		return best_move

	def mcts(self, board, player, iteration_count=100, mixing_hyperparameter=0.5):
		root = Node((-1,-1), 1, player, board)
		for it in range(0, iteration_count):
			history = set()
			leaf = root.traverse_to_leaf(history)
			leaf.expand(self)
			leaf_values = self.evaluate_turn_value(leaf.board, leaf.player)
			player_values = {1 : leaf_values[1], -1 : leaf_values[2]}
			rollout_result = leaf.play_rollout(self)
			for node in history:
				node.visit_count = node.visit_count + 1	
				node.value_sum = node.value_sum + (player_values[node.player] * mixing_hyperparameter + rollout_result * node.player * (1 - mixing_hyperparameter))
			
		move = None
		max_visit_count = 0
		for child_node in root.children:
			if child_node.visit_count > max_visit_count:
				max_visit_count = child_node.visit_count
				move = child_node.move
		return move
