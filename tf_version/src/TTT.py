import numpy as np
import random

"""
	Holds positionaly denoted pieces
	+1 => X
	-1 => O
	0 => empty
"""

class Board:
	def __init__(self, size):
		self.size = size;
		self.refresh()

	def refresh(self):
		self.board = np.zeros((self.size, self.size))
		self.col_sums = np.zeros(self.size)
		self.row_sums = np.zeros(self.size)
		self.left_diag = 0
		self.right_diag = 0;
		self.open_plays = set()
		for i in range(0, self.size):
			for j in range(0, self.size):
				self.open_plays.add((i, j))
				
	def place_piece(self, i, j, p):
		self.row_sums[i] += p
		self.col_sums[j] += p
		if(i == j):
			self.left_diag += p
		if(i + j == self.size-1):
			self.right_diag += p
		self.board[i][j] = p
		
		self.open_plays.remove((i, j));

	def remove_piece(self, i, j):
		self.col_sums[j] -= self.board[i][j]
		self.row_sums[i] -= self.board[i][j]
		if(i == j):
			self.left_diag -= self.board[i][j]
		if(i + j == self.size-1):
			self.right_diag -= self.board[i][j]
		self.board[i][j] = 0

		self.open_plays.add((i, j))

	def has_won(self):
		for i, val in enumerate(self.col_sums):
			if(abs(val) == self.size):
				return self.board[0][i]

		for i, val in enumerate(self.row_sums):
			if(abs(val) == self.size):
				return self.board[i][0]

		if(abs(self.left_diag) == self.size):
			return self.board[0][0]
		
		if(abs(self.right_diag) == self.size):
			return self.board[0][self.size-1]

		return 0

	def drawn(self):
		return not len(self.open_plays)

	def negamax(self, player, depth=0):
		winner = self.has_won()
		if(winner):
			return ((winner * player)/depth, (-1, -1))
		if(self.drawn()):
			return (0, (-1, -1))
		plays_to_check = list(self.open_plays)
		random.shuffle(plays_to_check) 
		best_score = -(1000000)
		best_play = (-1, -1)
		for play in plays_to_check:
			self.place_piece(play[0], play[1], player)
			potential_play = self.negamax(-player, depth+1);
			if(-potential_play[0] > best_score):
				best_score = -potential_play[0]
				best_play = play
			self.remove_piece(play[0], play[1])
		return (best_score, best_play)

	def print(self):
		for row in range(0, self.size):
			for col in range(0, self.size):
				print(str(self.board[row][col]) + " ", end='')
			print()
		print()

