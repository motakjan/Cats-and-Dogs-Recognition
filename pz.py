import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import pickle
import time

X = pickle.load(open("X.pickle","rb"))
y = pickle.load(open("y.pickle","rb"))

X = X/255.0
y = np.array(y)

dense_layers = [0]
layer_sizes = [64]
conv_layers = [3]

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            NAME = "{}-conv-{}-nodes-{}-dense-{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
            tensorboard = TensorBoard(log_dir='logs\{}'.format(NAME)) # tensorboard --logdir=logs\  shows tenderboard
            print(NAME)

            model = Sequential()
            model.add(Conv2D(layer_size,(3,3),input_shape = X.shape[1:]))
            model.add(Activation("relu"))
            model.add(MaxPooling2D(pool_size=(2,2)))

            for l in range(conv_layer-1):
                model.add(Conv2D(layer_size,(3,3),input_shape = X.shape[1:]))
                model.add(Activation("relu"))
                model.add(MaxPooling2D(pool_size=(2,2)))

            model.add(Flatten()) # converts 3D feature maps to 1D feature maps

            for l in range(dense_layer):
                model.add(Dense(layer_sizes))
                model.add(Activation('relu'))

            model.add(Dense(1))
            model.add(Activation('sigmoid'))

            model.compile(loss="binary_crossentropy", optimizer="adam",metrics=['accuracy'])

            model.fit(X, y, batch_size=32,epochs=11, validation_split=0.10, callbacks=[tensorboard])

model.save('64x3-CNN-new.model')