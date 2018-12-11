import tensorflow as tf
import numpy as np

import AlphaCheckers
import Checkers


def play_human_turn(board, player):
	while True:
		print("Please enter your move as checkers move coordinates: (ie. 11 15)")
		print("If unfamiliar with checkers coordiantes, see: https://webdocs.cs.ualberta.ca/~chinook/play/notation.html")
		print("Or enter 1 to end turn")
		move = []
		while not len(move):
			move = input().split()
		if len(move) == 1:
			return
		from_coord = int(move[0])
		to_coord = int(move[1])
		board.move_piece((from_coord, to_coord))	

board = Checkers.Board()
alpha_player = AlphaCheckers.Player()

board.show()
turn_count = 0
while not board.has_winner():
	print("Turn: ", turn_count)
	
	print("Black turn")
	play_human_turn(board, board.get_black_piece())
	board.show()

	print("White turn")
	alpha_moves = alpha_player.play_turn(board, board.get_white_piece())
	for move in alpha_moves:
		board.move_piece(move)
	board.show()

	turn_count = turn_count + 1

print("Winner: ", board.has_winner())
