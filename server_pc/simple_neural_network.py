# import the necessary packages
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

size = (32,24)

# grab the list of images that we'll be describing
print("[INFO] describing images...")
imagePaths = list(paths.list_images("dataTraining"))

# initialize the data matrix and labels list
data = []
labels = []

# loop over the input images
for (i, imagePath) in enumerate(imagePaths):
	# load the image and extract the class label (assuming that our
	# path as the format: /path/to/dataset/{class}.{image_num}.jpg
	image = cv2.imread(imagePath)
	label = imagePath.split(os.path.sep)[-1].split(".")[0]

	# construct a feature vector raw pixel intensities, then update
	# the data matrix and labels list
	features = cv2.resize(image, size).flatten()
	data.append(features)
	labels.append(label)
	
	print("[INFO] processed {}/{}".format(i, len(imagePaths)))

# encode the labels, converting them from strings to integers
le = LabelEncoder()
labels = le.fit_transform(labels)

# scale the input image pixels to the range [0, 1], then transform
# the labels into vectors in the range [0, num_classes] -- this
# generates a vector for each label where the index of the label
# is set to `1` and all other entries to `0`
data = np.array(data) / 255.0
labels = np_utils.to_categorical(labels, 3)	# Foward (1): [0,1,0,0] / Left (2): [0,0,1,0] / Right (3): [0,0,0,1]

# partition the data into training and testing splits, using 75%
# of the data for training and the remaining 25% for testing
print("[INFO] constructing training/testing split...")
(trainData, testData, trainLabels, testLabels) = train_test_split(data, labels, test_size=0.25, random_state=42)

# define the architecture of the network
model = Sequential()
model.add(Dense(576, input_dim=2304, init="uniform", activation="relu"))
model.add(Dense(288, init="uniform", activation="relu"))
model.add(Dense(3))
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
