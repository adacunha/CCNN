import tensorflow as tf
import numpy as np

import AlphaCheckers
import Checkers


def play_human_turn(board, player):
	while True:
		move = input().split()
		if len(move) == 1:
			return
		from_coord = int(move[0])
		to_coord = int(move[1])
		board.move_piece((from_coord, to_coord))	

board = Checkers.Board()
alpha_player = AlphaCheckers.Player()

while not board.has_winner():

	alpha_move = alpha_player.play_turn(board, board.get_black_piece())
	board.move_piece(alpha_move)

	play_human_turn()

print("Winner: ", board.has_winner())
