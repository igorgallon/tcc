# Picamera reference: http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# Socket reference: https://pymotw.com/2/socket/tcp.html
# Streaming by socket reference: http://picamera.readthedocs.io/en/release-1.9/recipes1.html#capturing-to-a-network-stream
# Struct referece: https://docs.python.org/2/library/struct.html

__author__ = 'Igor Gallon'

from keras.layers import Dense
from keras.models import model_from_json
from keras.models import load_model
from keras.optimizers import SGD
from keras.utils import np_utils
from Resolution import Resolution
from Messages import Messages
import numpy as np
import cv2
import picamera
import io
import time
import socket
import struct

class PredictingFrames(object):
    
    def __init__(self, serialPort):
               
        # Instantiate Serial comunication
        self.arduino = serialPort
        self.frameRate = 20    # 20 frames per second
        self.sizeFrame = Resolution(320, 240)
        self.sizeData = (32, 24)
        self.thresholdParam = 30
        self.numClasses = 4
        
        with open("model.json", "r") as json_file:
            print("[PREDICTION] Loading model...")
            model_json = json_file.read()
            self.model = model_from_json(model_json)
            
        print("[PREDICTION] Compiling model...")
        sgd = SGD(lr=0.01)
        self.model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
            
        print("[PREDICTION] Loading weights...")
        self.model.load_weights("model.h5")
        
        print("[PREDICTION] Model and Weights have been loaded successfully!")
        
    
    def convertToMessage(self, classification):
        classes = {
            0: Messages.msgBackward,
            1: Messages.msgForward,
            2: Messages.msgLeft,
            3: Messages.msgRight
        }
        
        return classes.get(classification, Messages.msgForward)
    
    
    def run(self):
        
        msg = ""
        direction = ""
        prob = []
        classification = 0
        
        print("[PREDICTION] Starting prediction...")
        try:
            
            # Initializing picamera
            with picamera.PiCamera() as camera:
                print("[PREDICTION] Initializing picamera...")
                # Sets the camera resolution
                camera.resolution = (self.sizeFrame.width, self.sizeFrame.height)
                camera.framerate = self.frameRate
                camera.start_preview()    # Start a preview
                time.sleep(2)  # Wait camera initializing (adjust luminosity or focus)
                
                stream = io.BytesIO()
                
                while 1:
                    
                    if self.arduino.inWaiting() > 0:
                        msg = self.arduino.readline()
                    
                    if msg == Messages.msgStop:
                        break
                    
                    try:
                        #Capture frame from camera
                        camera.capture(stream, format='jpeg')
                        image_mat = np.fromstring(stream.getvalue(), dtype=np.uint8)                    # Converting image stream array into may numpy format 
                        frame = cv2.imdecode(image_mat, 1)                                              # Decoding the image 
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                                 # Apply Gray filter (convert to 1-channel)
                        frame = cv2.threshold(frame, self.thresholdParam, 255, cv2.THRESH_BINARY)[1]    # Binarizing image (0 and 1 pixel values)                
                        frame = cv2.resize(frame, self.sizeData)                                        # Resize image
                        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB).flatten()                       # Convert image to RGB (3-channels) and flat into an 1D-array
                        array = np.array(frame)/255.0                                                   # Convert to numpy array and normalize pixel values from [0,255] to [0,1]
                        array = array[None, :]                                                          # Verticalize array
                        
                        prob = self.model.predict(array)                                                # Get the probabilities array from prediction of frame
                        # Get the index of max value in prabilities array
                        # Backward (0): [max, _, _, _] / Forward (1): [_, max, _, _] / Left (2): [_, _, max, _] / Right (3): [_, _, _, max]
                        classification = np.argmax(prob)
                        
                        direction = self.convertToMessage(classification)
                        print("[PREDICTION] Direction predicted {} Probabilities {} ".format(direction, prob))
                        
                        # Send direction to Arduino
                        self.arduino.write(direction)
                        
                    except Exception as e:
                        print(str(e))
                        
                    #Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()
                    
        except Exception as e:
            print(str(e))
        finally:
            print("[PREDICTION] Stopping... ")