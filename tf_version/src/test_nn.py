import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import seaborn as sns

import TTT

model = tf.keras.models.Sequential([
	layers.Dense(100, activation=tf.nn.relu),
	layers.Dense(100, activation=tf.nn.relu),
    	layers.Dense(9, activation=tf.nn.softmax)
])

checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
latest = tf.train.latest_checkpoint(checkpoint_dir)
model.load_weights(latest)

board = TTT.Board(3)

alpha_player = -1
nn_player = 1

nn_input = board.get_nn_input(nn_player)

nn_first_move = model.predict(np.array([nn_input]))

nn_first_move =  np.resize(nn_first_move, (3, 3))

#ax = sns.heatmap(nn_first_move, linewidth=0.05)
#plt.show()

board.refresh()
board.place_piece(1, 1, 1)
board.place_piece(0, 0, -1)
nn_invalid_test = model.predict(np.array([board.get_nn_input(nn_player)]))
nn_invalid_test = np.resize(nn_invalid_test, (3, 3))
#ax = sns.heatmap(nn_invalid_test, linewidth=0.05)
#plt.show()

game_count = 10000
alpha_count = 0
nn_count = 0

starting_player = alpha_player

for game_i in range(0, game_count):
	board.refresh()
	current_player = starting_player
	starting_player *= -1
	while(not board.has_won() and not board.drawn()):
		if(current_player == alpha_player):
			# optimal_move = board.negamax(alpha_player);	
			# board.place_piece(optimal_move[1][0], optimal_move[1][1], alpha_player)
			board.random_move(alpha_player)
		else:
			nn_guesses = model.predict(np.array([board.get_nn_input(nn_player)]))
			max_guess = -1
			max_index = -1
			for i, v in enumerate(nn_guesses[0]):
				if(v > max_guess):
					max_guess = v
					max_index = i	
			move_row = int(max_index / 3)
			move_col = max_index % 3
			board.place_piece(move_row, move_col, nn_player)
		current_player *= -1
	result = board.has_won()
	if(result == 1):
		nn_count += 1
	if(result == -1):
		alpha_count +=1

print("NN lost : " + str(alpha_count/game_count) + "% of games");
