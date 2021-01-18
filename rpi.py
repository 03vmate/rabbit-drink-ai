import sounddevice as adc
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from threading import Thread
import mysql.connector
import time
import math

#Connect to MySQL
db = mysql.connector.connect(host="127.0.0.1", user="pi", password="qwerty", database="DrinkAI")

#Load model
model = tf.keras.models.load_model('model/ai')

def process(data):
    global db
    unixtime = int(time.time())

    #Normalize data
    data = data / (np.max(data) if np.max(data) > abs(np.min(data)) else abs(np.min(data)))

    #Predict
    pred = model.predict(np.expand_dims(data,0))

    score = pred[0][1]-pred[0][0]

    #Write score to DB
    if(not math.isnan(score)):
        try:
            c = db.cursor()
            c.execute("INSERT INTO Drink (score, timestamp) VALUES (%s, %s)", (float(score), unixtime))
            db.commit()
        #Sometimes the db connection is broken, retry
        except Exception as e:
            print(e)
            db = mysql.connector.connect(host="127.0.0.1", user="pi", password="qwerty", database="DrinkAI")


thr = None
try:
    while(True):
        #Record 16000 samples (1sec) of audio from the microphone
        data = adc.rec(16000, samplerate=16000, channels=1).flatten()
        adc.wait()

        #Inference
        thr = Thread(target=process, args=(data,))
        thr.start()
except KeyboardInterrupt:
    print("Waiting for TF to finish...")
    thr.join()
    print("Exiting")
