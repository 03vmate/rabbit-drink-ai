# rabbit-drink-ai
Monitors water consumption of a pet by using a microphone to pick up audio, and TensorFlow to figure out if the pet is drinking or not

## Training

### preprocess.py
Converts audio files to 16ksps 1 second files

### ai_hypertune.py
Hyperparameter tuning

### ai.py
Model training

## Running on a RPi

### rpi.py
Runs detection

### live.py
Raspberry Pi Camera Server (https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming)

### ai.service
Systemd service for ai.py

### live.service
Systemd service for live.py

