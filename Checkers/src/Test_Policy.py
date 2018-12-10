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

names = {player_1 : "black", player_2 : "white", 0 : "draw"}

def play_nn_turn(board, player):
	move_guess = model.predict(np.array([board.get_cnn_input(player)]))[0]
	move_guess = board.clean_nn_guess(move_guess, player)
	move_guess = np.argmax(move_guess)
	move = board.parse_nn_output(move_guess, player, True)
	move_valid = move[0] == 1
	move_coords = move[1]
	if not move_valid:
		print("Invalid move by player: ", player, ": ", move_coords)
		return False
	log_str = ""
	capturing = board.is_capture(move_coords)
	board.move_piece(move_coords)	
	move_type_str = "x" if capturing else "->"
	log_str = log_str + str(move_coords[0]) + move_type_str + str(move_coords[1])
	while capturing:	
		move_guess = model.predict(np.array([board.get_cnn_input(player)]))[0]
		print("Before: ")
		print(move_guess)
		move_guess = board.clean_nn_guess(move_guess, player)
		print("After: ")
		print(move_guess)
		move_guess = np.argmax(move_guess)
		move_valid = move[0] == 1
		seq_move_coords = move[1]
		if not move_valid:
			print("Invalid seq jump: ", seq_move_coords)
			break	
		if seq_move_coords[0] != move_coords[1]:
			print("Disconnected seq jump: ", seq_move_coords)
			break
		if not board.is_capture(seq_move_coords):
			print("Non-Capture seq jump: ", seq_move_coords)
			break
		log_str = log_str + "x" + str(seq_move_coords[1])
		board.move_piece(seq_move_coords)	
		move_coords = seq_move_coords
	print(names[player], " ", log_str)
	board.show()
	return True

def play_human_turn(board, player):
	

board.show()
turn_count = 0
while not board.has_winner():
	if not play_nn_turn(board, player_1):
		break

	#if not play_nn_turn(board, player_2):
	#	break
	play_human_turn(board, player_2)

	turn_count = turn_count + 1
	if turn_count == 100:
		break
print("Winner: ", names[board.has_winner()], " in ", turn_count, " turns!")
