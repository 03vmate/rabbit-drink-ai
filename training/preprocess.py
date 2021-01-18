from scipy.io import wavfile
import numpy as np
import os
import random
import shutil

def initDir(name):
    if(os.path.isdir(name)):
        shutil.rmtree(name)
    os.mkdir(name)

initDir("temp")
initDir("processed")

for filename in os.listdir("raw/drink"):
    if(".wav" in filename):
        os.system("sox raw/drink/" + filename + " -r 16000 -c 1 -b 16 " + "temp/drink-" + filename)
for filename in os.listdir("raw/noise"):
    if(".wav" in filename):
        os.system("sox raw/noise/" + filename + " -r 16000 -c 1 -b 16 " + "temp/noise-" + filename)

for filename in os.listdir("temp"):
    if(".wav" in filename):
        samplerate, data = wavfile.read("temp/" + filename)
        arr = np.array(data)
        slicecounter = 0
        for i in range(int(len(arr) / samplerate)):
            _slice = arr[i * samplerate:(i+1)*samplerate]
            if("drink" in filename):
                wavfile.write("processed/" + filename[:-4] + "-" + str(slicecounter) + ".wav", samplerate, _slice)
            else:
                rand = random.randint(0, 4)
                if(rand == 0):
                    wavfile.write("processed/" + filename[:-4] + "-" + str(slicecounter) + ".wav", samplerate, _slice)
            slicecounter += 1
        wavfile.write("processed/" + filename[:-4] + "-" + str(slicecounter) + ".wav", samplerate, arr[-samplerate:])
shutil.rmtree("temp")