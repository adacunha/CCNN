import tensorflow as tf
import os
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

model_name = "64c_32c_1000r"

data = []
labels = []

train_data_file = "../data/parsed_games_small.txt"
with open(train_data_file) as dat_file:
	for line in dat_file:
		raw_data = line.strip().split()	
		x = [int(x) for x in raw_data[0:32]]
		y = [int(x) for x in raw_data[160:162]]
		data.append(np.array(x).reshape(8, 4, 1))
		labels.append(y)

data = np.array(data)
labels = np.array(labels)

model = tf.keras.models.Sequential([
	keras.layers.Conv2D(64, kernel_size=(2, 2), strides=(1, 1), activation='relu', input_shape=(8,4,1)),
	keras.layers.Conv2D(32, kernel_size=(2, 2), strides=(1, 1), activation='relu'),
	keras.layers.Flatten(),
    	keras.layers.Dense(1024, activation='relu'),
    	keras.layers.Dense(3, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss = 'categorical_crossentropy',
              metrics=['accuracy'])

checkpoint_path = "value_network_checkpoints/" + model_name + ".ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create checkpoint callback
# Create checkpoint callback
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1)

model.fit(data, labels, epochs=50, callbacks=[cp_callback])
