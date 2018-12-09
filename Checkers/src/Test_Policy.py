import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import seaborn as sns

import Checkers

test_model_name = "100r"

model = tf.keras.models.Sequential([
	layers.Dense(100, activation=tf.nn.relu),
    	layers.Dense(128, activation=tf.nn.softmax)
])

checkpoint_path = "policy_network_checkpoints/" + test_model_name + ".ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
latest = tf.train.latest_checkpoint(checkpoint_dir)
model.load_weights(latest)

board = Checkers.Board()

player_1 = board.get_black_piece()
player_2 = board.get_white_piece()

nn_input = board.get_nn_input(player_1)

nn_first_move = model.predict(np.array([nn_input]))[0]
first_move = np.argmax(predictions[0])
print(nn_first_move)
print(first_move)
