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
    	keras.layers.Dense(3, activation=tf.nn.softmax)
])

checkpoint_path = "value_network_checkpoints/" + test_model_name + ".ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
latest = tf.train.latest_checkpoint(checkpoint_dir)
model.load_weights(latest)

board = Checkers.Board()

player_1 = board.get_black_piece()
player_2 = board.get_white_piece()

board.refresh()

outcome_guess = model.predict(np.array([board.get_cnn_input(player_1)]))[0]
print(outcome_guess)

board.clear()

board.place_own_pawn(player_1, 1)
board.place_opponent_pawn(player_1, 5)
board.place_opponent_king(player_1, 7)
board.place_opponent_king(player_1, 15)
board.place_own_king(player_1, 32)
board.place_own_king(player_1, 29)
board.place_opponent_king(player_1, 20)

outcome_guess = model.predict(np.array([board.get_cnn_input(player_1)]))[0]
print(outcome_guess)
