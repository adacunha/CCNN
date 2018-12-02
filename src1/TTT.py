import numpy as np

"""
	Holds positionaly denoted pieces
	+1 => X
	-1 => O
	0 => empty
"""

class Board:
	def __init__(self, size):
		self.size = size;
		self.board = np.zeros((size, size))

		self.col_sums = np.zeros(size)
		self.row_sums = np.zeros(size)

		self.left_diag = 0
		self.right_diag = 0

	def can_place_at(self, i, j):
		return not self.board[i][j]
				
	def place_piece(self, i, j, p):
		self.row_sums[i] += p
		self.col_sums[j] += p
		if(i == j):
			self.left_diag += p
		if(i + j == self.size-1):
			self.right_diag += p
		self.board[i][j] = p

	def remove_piece(self, i, j):
		self.col_sums[j] -= self.board[i][j]
		self.row_sums[i] -= self.board[i][j]
		if(i == j):
			self.left_diag -= self.board[i][j]
		if(i + j == self.size-1):
			self.right_diag -= self.board[i][j]
		self.board[i][j] = 0

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
