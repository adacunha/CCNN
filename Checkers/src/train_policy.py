import tensorflow as tf
import os
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

model_name = "100r_100r_100r"

data = []
labels = []

train_data_file = "../data/parsed_games.txt"
with open(train_data_file) as dat_file:
	for line in dat_file:
		raw_data = line.strip().split()	
		x = [int(x) for x in raw_data[0:32]]
		y = [int(y) for y in raw_data[32:160]]
		data.append(x)
		labels.append(y)

data = np.array(data)
labels = np.array(labels)

print(data)
print(labels)

model = tf.keras.models.Sequential([
	keras.layers.Dense(100, activation=tf.nn.relu),
	keras.layers.Dense(100, activation=tf.nn.relu),
	keras.layers.Dense(100, activation=tf.nn.relu),
    	keras.layers.Dense(128, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss = 'categorical_crossentropy',
              metrics=['accuracy'])

checkpoint_path = "policy_network_checkpoints/" + model_name + ".ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create checkpoint callback
# Create checkpoint callback
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1)

model.fit(data, labels, epochs=10, callbacks=[cp_callback])
