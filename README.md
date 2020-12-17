# rabbit-drink-ai

## Training

### preprocess.py
Training set 16ksps-re atalakitasa, 1mp-es reszekre vagasa

### ai_hypertune.py
Legjobb hyperparameterek keresese

### ai.py
Model training es mentes

## Raspberry Pi-on futo

### rpi.py
Mentett model segitsegevel felismeres elvegzese

### live.py
Kamera MJPEG szerver (modositott pelda kod innen: https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming)

### ai.service
Systemd service az AI inditasahoz

### live.service
Systemd service a kamera szerver inditasahoz

