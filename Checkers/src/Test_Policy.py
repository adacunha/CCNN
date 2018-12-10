import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import seaborn as sns

import Checkers

test_model_name = "64c_32c_1000r"

model = tf.keras.models.Sequential([
	keras.layers.Conv2D(64, kernel_size=(2, 2), strides=(1, 1), activation='relu', input_shape=(8,4,1)),
	keras.layers.Conv2D(32, kernel_size=(2, 2), strides=(1, 1), activation='relu'),
	keras.layers.Flatten(),
    	keras.layers.Dense(1024, activation='relu'),
    	keras.layers.Dense(128, activation=tf.nn.softmax)
])

checkpoint_path = "policy_network_checkpoints/" + test_model_name + ".ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
latest = tf.train.latest_checkpoint(checkpoint_dir)
model.load_weights(latest)

board = Checkers.Board()

player_1 = board.get_black_piece()
player_2 = board.get_white_piece()

board.show()

while not board.has_winner():

	black_move_guess = np.argmax(model.predict(np.array([board.get_cnn_input(player_1)]))[0])
	black_move = board.parse_nn_output(black_move_guess, player_1, True)
	black_move_valid = black_move[0]
	black_move_coords = black_move[1]
	if black_move_valid == -1:
		print("Invalid black move: ", black_move)
		break
	board.move_piece(black_move_coords)
	board.show()
	print("Black: ", black_move_coords)

	white_move_guess = np.argmax(model.predict(np.array([board.get_cnn_input(player_2)]))[0])
	white_move = board.parse_nn_output(white_move_guess, player_2, True)
	white_move_valid = white_move[0]
	white_move_coords = white_move[1]
	if white_move_valid == -1:
		print("Invalid white move: ", white_move)
		break
	board.move_piece(white_move_coords)
	board.show()
	print("White: ", white_move_coords)

print("Winner: ", board.has_winner())

def play_turn(board, player):
	move_guess = np.argmax(model.predict(np.array([board.get_cnn_input(player)]))[0])
	move = board.parse_nn_output(move_guess, player, True)
	move_valid = move[0] == 1
	move_coords = move[1]
	if not move_valid:
		print("Invalid move by player: ", player)
		return False
	capturing = board.move_piece(move_coords)	
	while capturing:	
		move_guess = model.predict(np.array([board.get_cnn_input(player)]))[0]
		
		
		


