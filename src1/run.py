import tensorflow as tf
import numpy as np
from tensorflow.keras import layers
import matplotlib.pyplot as plt

import TTT

board = TTT.Board(3);

start_player = 1

current_player = start_player
while(not board.has_won() and not board.drawn()):
	print(board.open_plays)
	best_play = board.negamax(current_player)
	board.place_piece(best_play[1][0], best_play[1][1], current_player)
	current_player *= -1
	board.print()

if(board.has_won() != 0):
	print("NEGAMAX ERROR!")
