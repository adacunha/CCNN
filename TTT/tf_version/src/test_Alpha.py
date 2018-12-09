import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import seaborn as sns

import TTT
import Alpha

alpha = Alpha.Alpha(64, "policy_network_checkpoints/1_64.ckpt", 64, "value_network_checkpoints/1_64.ckpt")

board = TTT.Board(3)

print(alpha.get_move(board, 1))

alpha_player = 1
other_player = -1

game_count = 100
alpha_count = 0
other_count = 0
draw_count = 0

starting_player = alpha_player

for game_i in range(0, game_count):
	board.refresh()
	current_player = starting_player
	starting_player *= -1
	while(not board.has_won() and not board.drawn()):
		if(current_player == alpha_player):
			alpha_move = alpha.get_move(board, current_player);
			board.place_piece(alpha_move[0], alpha_move[1], current_player)
		else:
			#optimal_move = board.negamax(current_player);	
			#board.place_piece(optimal_move[1][0], optimal_move[1][1], current_player)
			board.random_move(current_player)
		current_player *= -1
	result = board.has_won()
	print("Starting player: " + str(starting_player))
	if(result == 1):
		print("Alpha WON!")
		alpha_count += 1
	if(result == -1):
		print("Other WON!")
		other_count += 1
	if(result == 0):
		draw_count += 1
		print("DRAW!")

print("Alpha won : " + str(alpha_count*100/game_count) + "% of games");
print("Other won : " + str(other_count*100/game_count) + "% of games");
print("Draw: " + str(draw_count*100/game_count) + "% of games");
