# References: http://www.pyimagesearch.com/2016/09/26/a-simple-neural-network-with-python-and-keras/
# imutils library reference: https://github.com/jrosebr1/imutils

from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Activation
from keras.optimizers import SGD
from keras.layers import Dense
from keras.utils import np_utils
from imutils import paths
import numpy as np
import argparse
import cv2
import os

size = (32,24)								# Size of imported images (10x smaller than original)
numClasses = 4								# Foward / Left / Right / Backward
testSize = 0.25								# 25% of data destinated to test set

# Gets list of images from './dataTraining' path
print("Getting list of images...")
imageList = list(paths.list_images("./dataTraining"))

# Data and labels
data = []
labels = []

# Load images into 'data' and extracts the class label into 'labels'
for (i, img) in enumerate(imageList):
	image = cv2.imread(img)						# Reads the image
	imageRawVector = cv2.resize(image, size).flatten()		# Creates a vector of raw pixel intensities (length = w*h*3) - RGB
	data.append(imageRawVector)					# Appends image as vector format
	
	label = img.split(os.path.sep)[-1].split(".")[0]		# Extracts the class label in the format: 'data_training/{class_label}.{image_num}.jpg'
	labels.append(int(label))					# Appends label as integer

	print("Processed {} images of {}".format(i, len(imageList)))


data = np.array(data) / 255.0
labels = np_utils.to_categorical(labels, numClasses)	# Foward (1): [1,0,0,0] / Left (2): [0,1,0,0] / Right (3): [0,0,1,0] / Backward (0): [0,0,0,1]

print("Partitioning data in training/testing split...")
(trainData, testData, trainLabels, testLabels) = train_test_split(data, labels, test_size=testSize, random_state=42)

# Modeling the network
model = Sequential()
model.add(Dense(576, input_dim=2304, init="uniform", activation="relu"))
model.add(Dense(288, init="uniform", activation="relu"))
model.add(Dense(4))
model.add(Activation("softmax"))

# train the model using SGD
print("[INFO] compiling model...")
sgd = SGD(lr=0.01)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
model.fit(trainData, trainLabels, nb_epoch=50, batch_size=128, verbose=1)

# show the accuracy on the testing set
print("[INFO] evaluating on testing set...")
(loss, accuracy) = model.evaluate(testData, testLabels, batch_size=128, verbose=1)
print("[INFO] loss={:.4f}, accuracy: {:.4f}%".format(loss, accuracy * 100))

# Save Keras model in file
json_model = model.to_json()
with open("model.json", "w") as json_file:
	json_file.write(json_model);

# Save weights
model.save_weights("model.h5")
print("Model and weights saved to disk!")

# USAGE
# python simple_neural_network.py --dataset kaggle_dogs_vs_cats
