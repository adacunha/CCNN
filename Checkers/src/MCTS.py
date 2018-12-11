import numpy as np

class Node:
	def __init__(self, move, prior, player, board):
		self.move = move
		self.prior = prior
		self.visit_count = 0
		self.value_sum = 0
		self.board = board	
		self.player = player
		self.children = set()	

	def get_exploration_score(self):
		return 90*self.prior / (1 + self.visit_count)

	def get_exploitation_score(self):
		if self.visit_count == 0:
			return 0
		return self.value_sum / self.visit_count	

	def get_score(self):
		return self.get_exploration_score() + self.get_exploitation_score()

	def is_expanded(self):
		return not len(self.children) == 0

	def traverse_to_leaf(self, history):
		history.add(self)
		if not self.is_expanded():
			return self	
		best_child = None
		best_score = -1
		for child_node in self.children:
			child_score = child_node.get_score()
			if child_score > best_score:
				best_score = child_score
				best_child = child_node
		return best_child.traverse_to_leaf(history)

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
		while not play_board.has_winner() and not play_board.is_drawn():
			move_priors = alpha.evaluate_turn_policy(play_board, current_player)	
			max_index = -1
			max_prior = -1
			for index, prior in enumerate(move_priors):
				if prior > max_prior:
					max_prior = prior
					max_index = index
			move = play_board.parse_nn_output(max_index, current_player)[1]
			play_board.move_piece(move)
			current_player = play_board.get_next_player(current_player)
		win_state = play_board.has_winner()
		if win_state:
			return win_state
		if play_board.is_drawn():
			state_values = alpha.evaluate_turn_value(play_board, current_player)	
			win_code = np.argmax(state_values)
			if win_code == 0:
				return 0
			if win_code == 1:
				return 1
			return -1
