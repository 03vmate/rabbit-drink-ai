import sounddevice as adc
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from threading import Thread

model = tf.keras.models.load_model('model/ai')

def process(data):
    data = data / (np.max(data) if np.max(data) > abs(np.min(data)) else abs(np.min(data)))
    pred = model.predict(np.expand_dims(data,0))
    if(pred[0][0] > pred[0][1]):
        print("Not drinking")
    else:
        print("Drinking")
    print(pred)

thr = None
try:
    while(True):
        data = adc.rec(16000, samplerate=16000, channels=1).flatten()
        adc.wait()
        thr = Thread(target=process, args=(data,))
        thr.start()
except KeyboardInterrupt:
    print("Waiting for TF to finish...")
    thr.join()
    print("Exiting")