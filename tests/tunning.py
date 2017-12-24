# References: http://www.pyimagesearch.com/2016/09/26/a-simple-neural-network-with-python-and-keras/
# imutils library reference: https://github.com/jrosebr1/imutils

from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Activation
from keras.optimizers import SGD
from keras.layers import Dense
from keras.utils import np_utils
from imutils import paths
import numpy as np
import time
import cv2
import os

def create_model(nodes1=72, nodes2=36, activation='relu'):
    # Modeling the network
    model = Sequential()
    model.add(Dense(nodes1, input_dim=2304, init="uniform", activation=activation))
    model.add(Dense(nodes2, init="uniform", activation=activation))
    model.add(Dense(4))
    model.add(Activation('softmax'))
    sgd = SGD(lr=0.01)
    model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
    
    return model

if __name__ == '__main__':
    size = (32,24) # Size of imported images (10x smaller than original)
    testSize = 0.25 # 25% of data destinated to test set
    numClasses = 4
    
    # Hyperparameter space
    batch_size = [10, 40, 80, 128]
    epochs = [10, 50, 100]
    activationHidden = ['relu', 'sigmoid', 'softmax']
    #activationOutput = ['relu', 'sigmoid', 'softmax']
    #optimizer = ['sgd', 'adam', 'rmsprop', 'adagrad', 'adadelta',  'adamax', 'nadam', 'tfoptimizer']
    optimizers = ['sgd', 'adam', 'adamax']
    nodes1  = [1152, 576, 288, 144, 72]
    nodes2 = [576, 288, 144, 72, 36]
    nodes3 = [288, 144, 72, 36, 18]
    
    param_grid = dict(batch_size=batch_size, epochs=epochs, activation=activationHidden, nodes1=nodes1, nodes2=nodes2)
    
    # Data and labels
    data = []
    labels = []		
    
    print("Loading the input data...")
    # Gets list of images from './dataTraining' path
    imageList = list(paths.list_images("./dataTraining"))
    
    # Load images into 'data' and extracts the class label into 'labels'
    for (i, img) in enumerate(imageList):
        image = cv2.imread(img)		# Reads the image
        # Creates a vector of raw pixel intensities (length = w*h*3) - RGB
        imageRawVector = cv2.resize(image, size).flatten()
        data.append(imageRawVector)	# Appends image as vector format
        # Extracts the class label in the format: 'data_training/{class_label}.{image_num}.jpg'
        label = img.split(os.path.sep)[-1].split(".")[0]
        labels.append(int(label))   # Appends label as integer
    # Converts the pixel values from [0, 255.0] to [0, 1] interval
    data = np.array(data) / 255.0 
    # Backward (0): [1,0,0,0] / Foward (1): [0,1,0,0] / Left (2): [0,0,1,0] / Right (3): [0,0,0,1]
    labels = np_utils.to_categorical(labels, numClasses)
    
    print("Spliting data training...")
    (trainData, testData, trainLabels, testLabels) = train_test_split(data, labels, test_size=testSize)
    
    seed = 7
    np.random.seed(seed)
    
    print("Defining the grid search parameters...")
    model = KerasClassifier(build_fn=create_model, verbose=0)
    print("Tuning hyperparameters via grid search (exhaustive method) - parallel mode")
    grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=4)
    print("Fitting data...")
    
    try:
        start = time.time()
        grid_result = grid.fit(trainData, trainLabels)
        print("Grid search took {:.2f} seconds".format(time.time() - start))
    except Exception as e:
        print(str(e))
        
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))