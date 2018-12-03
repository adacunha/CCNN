import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

train_file = open("games_train.dat", 'r')

data = []
labels = []

for line in train_file:
	raw_dat = list(map(int, map(float, line.split(" "))))
	t = [0 for i in range(0, 27)]
	for i in range(0, 9):
		if(raw_dat[i] == 0):
			t[i*3] = 1
		if(raw_dat[i] == 1):
			t[i*3+1] = 1	
		if(raw_dat[i] == -1):
			t[i*3+2] = 1
	data.append(t)
	labels.append([1 if raw_dat[9] == i else 0 for i in range(0, 9)])

data = np.array(data)
labels = np.array(labels)

print(data[0])
print(labels[0])

model = tf.keras.models.Sequential([
	keras.layers.Dense(100, activation=tf.nn.relu),
	keras.layers.Dense(100, activation=tf.nn.relu),
    	keras.layers.Dense(9, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss = 'categorical_crossentropy',
              metrics=['accuracy'])

model.fit(data, labels, epochs=1, callbacks = [cp_callback])
model.save_weights('nn_weights')


