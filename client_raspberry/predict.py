# Picamera reference: http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# Socket reference: https://pymotw.com/2/socket/tcp.html
# Streaming by socket reference: http://picamera.readthedocs.io/en/release-1.9/recipes1.html#capturing-to-a-network-stream
# Struct referece: https://docs.python.org/2/library/struct.html

__author__ = 'Igor Gallon'

from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.optimizers import SGD
import numpy
from Resolution import Resolution
from Messages import Messages
import io


class PredictingFrames(object):
    
    def __init__(self):
               
        # Instantiate Serial comunication
        self.sizeImg = Resolution(320,240)
        self.thresholdParam = 70
        
        print("[PREDICTION] Loading model and weights...")
        with open("model.json", "r") as json_file:
            print("read file")
            model_json = json_file.read()
            print("load model")
            self.model = model_from_json(model_json)
            print("compile model")
            sgd = SGD(lr=0.01)
            self.model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
            
            print("load weights")
            self.model.load_weights("model.h5")
        
        print("[PREDICTION] Model and Weights have been loaded!")            
        
        print("Success!")
    
