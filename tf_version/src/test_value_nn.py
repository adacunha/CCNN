import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import seaborn as sns

import TTT

model = tf.keras.models.Sequential([
	layers.Dense(64, activation=tf.nn.relu),
    	layers.Dense(9, activation=tf.nn.softmax)
])
checkpoint_path = "value_network_checkpoints/1_64.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
latest = tf.train.latest_checkpoint(checkpoint_dir)
model.load_weights(latest)

board = TTT.Board(3)

alpha_player = -1
nn_player = 1

board.place_piece(0, 0, -1)
board.place_piece(1, 0, 1)
board.place_piece(0, 1, -1)
board.place_piece(2, 0, 1)

if(model.predict(np.array([board.get_nn_input(nn_player)]))[0] != 1):
	print("VALUE ERROR")

board.refresh()

print(model.predict(np.array([board.get_nn_input(nn_player)])))
