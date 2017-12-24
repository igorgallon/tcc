# References: http://www.pyimagesearch.com/2016/09/26/a-simple-neural-network-with-python-and-keras/
# imutils library reference: https://github.com/jrosebr1/imutils

from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from keras.models import Sequential
from keras.models import model_from_json
from keras.models import load_model
from keras.layers import Activation
from keras.optimizers import SGD
from keras.layers import Dense
from keras.utils import np_utils
from imutils import paths
import numpy as np
import argparse
import cv2
import os

class TrainingNeuralNetwork(object):
	
	def __init__(self):
		# Size of imported images (10x smaller than original)
		self.size = (32,24)
		self.numClasses = 4 # Foward / Left / Right / Backward
		self.testSize = 0.25 # 25% of data destinated to test set
		
		self.nNodesInput = 32*24*3
		self.nNodesOutput = self.numClasses
		self.actvFunHidden = "relu"

		# Data and labels
		self.data = []
		self.labels = []		
	
	
	def run(self):
		# Gets list of images from './dataTraining' path
		print("[NEURAL NETWORK] Getting list of images from 'dataTraining' folder...")
		imageList = list(paths.list_images("./dataTraining"))
		
		# Load images into 'data' and extracts the class label into 'labels'
		for (i, img) in enumerate(imageList):
			image = cv2.imread(img)						# Reads the image
			imageRawVector = cv2.resize(image, self.size).flatten()		# Creates a vector of raw pixel intensities (length = w*h*3) - RGB
			self.data.append(imageRawVector)				# Appends image as vector format
			
			label = img.split(os.path.sep)[-1].split(".")[0]		# Extracts the class label in the format: 'data_training/{class_label}.{image_num}.jpg'
			self.labels.append(int(label))					# Appends label as integer
			
			print("[NEURAL NETWORK] Processed {} images of {}".format(i, len(imageList)))
		
		self.data = np.array(self.data) / 255.0					# Converts the pixel values from [0, 255.0] to [0, 1] interval
		self.labels = np_utils.to_categorical(self.labels, self.numClasses)	# Backward (0): [1,0,0,0] / Foward (1): [0,1,0,0] / Left (2): [0,0,1,0] / Right (3): [0,0,0,1]
		
		print("[NEURAL NETWORK] Partitioning data in training (75%) / testing split (25%)...")
		(trainData, testData, trainLabels, testLabels) = train_test_split(self.data, self.labels, test_size=self.testSize)
		
		np.random.seed(7)
		
		# Modeling the network
		model = Sequential()
		model.add(Dense(576, input_dim=self.nNodesInput, init="uniform", activation=self.actvFunHidden))
		model.add(Dense(32, init="uniform", activation=self.actvFunHidden))
		model.add(Dense(self.nNodesOutput))
		model.add(Activation("softmax"))
		
		# Train the model using SGD
		print("[NEURAL NETWORK] Compiling model...")
		sgd = SGD(lr=0.01)
		model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
		
		print("[NEURAL NETWORK] Training model...")
		model.fit(trainData, trainLabels, validation_set=0.2, nb_epoch=50, batch_size=128, verbose=1, shuffle=False)
		
		# Show the accuracy on the testing set
		print("[NEURAL NETWORK] Evaluating on testing set...")
		(loss, accuracy) = model.evaluate(testData, testLabels, batch_size=128, verbose=1)
		print("[NEURAL NETWORK] Loss={:.4f}, Accuracy: {:.2f}%".format(loss, accuracy * 100))
		
		self.data = []
		self.labels = []
		
		return model
	
	def save(self, model):
		# Save Keras model in file
		json_model = model.to_json()
		with open("model.json", "w") as json_file:
			json_file.write(json_model);
			
		# Save weights
		model.save_weights("model.h5")
		
		print("[NEURAL NETWORK] Model and weights saved to disk!")