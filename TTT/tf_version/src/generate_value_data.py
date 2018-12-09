import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers

import TTT

output_file = open("value_data.dat", 'w')

model = tf.keras.models.Sequential([
	layers.Dense(9, activation=tf.nn.relu),
    	layers.Dense(9, activation=tf.nn.softmax)
])

checkpoint_path = "checkpoints/1_9_random_real.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
latest = tf.train.latest_checkpoint(checkpoint_dir)
model.load_weights(latest)

board = TTT.Board(3)

player_nn = 1
player_alpha = -1

starting_player = player_nn

game_count = 100000

for game_i in range(0, game_count):
	board.refresh()
	current_player = starting_player
	starting_player *= -1
	game_states = []
	while(not board.has_won() and not board.drawn()):
		if(current_player == player_nn):
			c_p = [current_player]
			c_p.extend(board.get_nn_input(current_player));
			game_states.append(c_p)
			nn_guesses = model.predict(np.array([board.get_nn_input(current_player)]))
			tot_prob = 0
			for i, v in enumerate(nn_guesses[0]):
				row = int(i / 3)
				col = i % 3
				if(not board.is_valid_move(row, col)):
					nn_guesses[0][i] = 0
				else:
					tot_prob += nn_guesses[0][i]
			max_guess = -1
			max_index = -1
			for i, v in enumerate(nn_guesses[0]):
				if(v > max_guess):
					max_guess = v #/total_prob
					max_index = i	
			move_row = int(max_index / 3)
			move_col = max_index % 3
			board.place_piece(move_row, move_col, current_player)
		else:
			board.random_move(current_player);
		current_player *= -1
	result = board.has_won()
	for state in game_states:
		for piece in state[1:]:
			output_file.write(str(piece) + " ")
		did_win = 1 if result == state[0] else -1 
		output_file.write(str(did_win) + "\n")
