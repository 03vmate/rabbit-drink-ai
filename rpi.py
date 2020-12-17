import sounddevice as adc
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from threading import Thread
import mysql.connector
import time
import math

db = mysql.connector.connect(host="127.0.0.1", user="pi", password="qwerty", database="DrinkAI")

model = tf.keras.models.load_model('model/ai')

lastTimestamp = 0

def process(data):
    global lastTimestamp
    global db
    unixtime = int(time.time())
    data = data / (np.max(data) if np.max(data) > abs(np.min(data)) else abs(np.min(data)))
    pred = model.predict(np.expand_dims(data,0))

    score = pred[0][1]-pred[0][0]
    if(not math.isnan(score)):
        try:
            c = db.cursor()
            if(lastTimestamp != 0):
                if(unixtime - lastTimestamp > 1):
                    for i in range(int((unixtime - lastTimestamp) - 1)):
                        c.execute("INSERT INTO Drink (score, timestamp) VALUES (%s, %s)", (float(score), lastTimestamp + i + 1))
            c.execute("INSERT INTO Drink (score, timestamp) VALUES (%s, %s)", (float(score), unixtime))
            lastTimestamp = unixtime
            db.commit()
        except Exception as e:
            print(e)
            db = mysql.connector.connect(host="127.0.0.1", user="pi", password="qwerty", database="DrinkAI")


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
