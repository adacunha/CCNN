import tensorflow as tf
import numpy as np
from tensorflow.keras import layers
import matplotlib.pyplot as plt

import time

import TTT

board = TTT.Board(3);

board.place_piece(1, 1, 1);
board.place_piece(1, 0, 1);
board.place_piece(1, 2, 1);

if(1 != board.has_won()):
	print("BOARD WIN ERROR 1")

board.remove_piece(1, 1);
if(1 == board.has_won()):
	print("BOARD REMOVE WIN ERRROR")

board.place_piece(2, 0, -1);
board.place_piece(1, 1, -1);
board.place_piece(0, 2, -1);
if(-1 != board.has_won()):
	print("BOARD REPLACE ERROR");

board.remove_piece(0, 2);
board.place_piece(0, 0, -1);
board.place_piece(0, 2, -1)

if(-1 != board.has_won()):
	print("WTF")


board.refresh()
test_play = board.negamax(1);
if(test_play[0] != 0):
	print("NEGAMAX VALUE ERROR: " + str(test_play[0]))

board.refresh()
test_play = board.negamax(-1);
if(test_play[0] != 0):
	print("NEGAMAX VALUE ERROR: " + str(test_play[0]))

start = time.time()
start_player = 1;
for i in range(0, 10):
	board.refresh()
	start_player *= -1
	current_player = start_player
	while(not board.has_won() and not board.drawn()):
		best_play = board.negamax(current_player)
		board.place_piece(best_play[1][0], best_play[1][1], current_player)
		current_player *= -1
	board.print()
	if(board.has_won() != 0):
		print("NEGAMAX ERROR!")
end = time.time()
print(end - start)
