import numpy as np
import tensorflow as tf

import TTT

model = tf.keras.models.Sequential([
	keras.layers.Dense(100, activation=tf.nn.relu),
	keras.layers.Dense(100, activation=tf.nn.relu),
    	keras.layers.Dense(9, activation=tf.nn.softmax)
])

model.load_weights('nn_weights')

board = TTT.Board




