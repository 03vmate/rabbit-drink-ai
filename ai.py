from scipy.io import wavfile
import numpy as np
import random
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import regularizers
import kerastuner as kt
import os
import shutil

config = tf.compat.v1.ConfigProto(gpu_options =  tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8))
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(session)

trainingData = []
trainingLabels = []

testData = []
testLabels = []

trainingCount_noise = 0
trainingCount_drinking = 0
testCount_noise = 0
testCount_drinking = 0

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

def dataAppend(data, label):
    global trainingCount_drinking, trainingCount_noise, testCount_drinking, testCount_noise
    rand = random.randint(0, 9)
    if(rand == 0):
        testData.append(data)
        testLabels.append(label)
        if(label == 0):
            testCount_noise += 1
        else:
            testCount_drinking += 1
    else:
        trainingData.append(data)
        trainingLabels.append(label)
        if(label == 0):
            trainingCount_noise += 1
        else:
            trainingCount_drinking += 1

for filename in os.listdir("processed"):
    filename = "processed/" + filename
    if(".wav" in filename):
        s, data = wavfile.read(filename)
        _data = np.array(data)
        div = np.max(_data) if np.max(_data) > abs(np.min(_data)) else abs(np.min(_data))
        _data = _data / div
        if("noise" in filename):
            dataAppend(_data, 0)
        if("drink" in filename):
            dataAppend(_data, 1)

print("Training set size: " + str(trainingCount_noise) + "/" + str(trainingCount_drinking))
print("Test set size: " + str(testCount_noise) + "/" + str(testCount_drinking))

_trainingData = np.array(trainingData)
_trainingLabels = np.array(trainingLabels)
_testData = np.array(testData)
_testLabels = np.array(testLabels)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.0001)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.0001)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(2)
])

model.compile(tf.keras.optimizers.Adam(learning_rate = 0.01),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(_trainingData, _trainingLabels, epochs=10)

test_loss, test_acc = model.evaluate(_testData,  _testLabels, verbose=2)
print('\nTest accuracy:', test_acc)

model.save("model/ai")