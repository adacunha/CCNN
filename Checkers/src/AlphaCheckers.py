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
		
	def evaluate_turn_policy(self, board, player):
		move_guess = self.policy_network.predict(np.array([board.get_cnn_input(player)]))[0]
		move_guess = board.clean_nn_guess(move_guess, player)
		return move_guess
	
	def evaluate_turn_value(self, board, player):
		outcome_guess = self.value_network.predict(np.array([board.get_cnn_input(player)]))[0]
		return outcome_guess

	def play_turn(self, board):
		best_move = self.mcts(board)

	class Node:
		def __init__(self, move, prior, player, board):
			self.move = move
			self.prior = prior
			self.visit_count = 0
			self.value_sum = 0
			self.board = board	
			self.player = player
			self.children = set()	

		def get_exporation_score(self):
			return self.prior / (1 + self.visit_count)

		def get_exploitation_score(self):
			if self.visit_count == 0:
				return 0
			return self.value_sum / self.visit_count	

		def get_score(self):
			return self.get_exploration_score() + self.get_exploitation_score()

		def is_expanded(self):
			return len(self.children) > 0
		def is_leaf(self):
			return not self.is_expanded()

		def traverse_to_leaf(self, history):
			history.add(self)
			if not self.is_leaf():
				return self
			best_child = None
			best_score = -1
			for child_node in self.children:
				child_score = child_node.get_score()
				if child_score > best_score:
					best_score = child_score
					best_child = child_node
			return best_child.traverse_to_leaf()

		def expand(self, alpha):
			priors = alpha.evaluate_turn_policy(self.board, self.player)
			next_player = self.board.get_next_player(self.player)
			for index, prior in enumerate(priors):
				if prior == 0:
					continue
				move_coords = self.board.parse_nn_output(index, self.player, True)[1]
				next_board = self.board.deep_copy()

				## TODO multiple jump moves

				next_board.move_piece(move_coords)
				new_child = Node(move_coords, prior, next_player, next_board)	
				self.children.add(new_child)

		def play_rollout(self, alpha):
			play_board = self.board.deep_copy()
			current_player = self.player
			while not self.board.has_winner() and not self.board.is_drawn():
				move_priors = alpha.evaluate_turn_policy(play_board, current_player)	
				max_index = -1
				max_prior = -1
				for index, prior in enumerate(move_priors):
					if prior > max_prior:
						max_prior = prior
						max_index = index
				move = play_board.parse_nn_output(index, current_player)[1]
				play_board.move_piece(move)
				current_player = play_board.get_next_player(current_player)
			win_state = self.board.has_winner()
			if win_state:
				return win_state
			if self.board.is_drawn():
				state_values = alpha.evaluate_turn_value(play_board, current_player)	
				win_code = np.argmax(state_values)
				if win_code == 0:
					return 0
				if win_code == 1:
					return 1
				assert(win_code == -1)
				return -1
	
	def mcts(self, board, iteration_count, mixing_hyperparameter=0.5):
		root = Node((-1,-1), 1, self.player, board)
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
