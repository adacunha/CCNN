import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

model_name = "1_64"

train_file = open("value_data.dat", 'r')

data = []
labels = []

for line in train_file:
	raw_dat = list(map(int, map(float, line.split(" "))))
	data.append(raw_dat[0:27])
	labels.append(raw_dat[27])

data = np.array(data)
labels = np.array(labels)

model = keras.Sequential([ keras.layers.Dense(64, activation=tf.nn.relu), 
			keras.layers.Dense(1)])

model.compile(loss='mse', optimizer=tf.train.RMSPropOptimizer(0.001), metrics=['mae'])

checkpoint_path = "value_network_checkpoints/" + model_name + ".ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create checkpoint callback
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1)

model.fit(data, labels, epochs=10,
                    validation_split=0.2,
                    callbacks=[cp_callback])
