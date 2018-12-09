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

cnn_input = board.get_cnn_input(player_1)

network_input = []
network_input.append(cnn_input)
network_input = np.array(network_input)

predictions = model.predict(network_input)

first_move_guess = np.argmax(predictions[0])
first_move_coords = board.parse_nn_output(first_move_guess)
print("First move: ", board.parse_nn_output(first_move_guess))
board.move_piece(first_move_coords)

network_input = np.array([board.get_cnn_input(player_2)])
second_move_guess = np.argmax(model.predict(network_input))
second_move_coords = board.parse_nn_output(second_move_guess)
print("Second move: ", second_move_coords)
board.move_piece(second_move_coords)

