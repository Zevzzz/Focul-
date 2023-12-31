
import numpy as np
from keras.models import Sequential
from keras import layers
from keras.optimizers import Adam
from keras.regularizers import l1, l2
from keras.callbacks import ModelCheckpoint, CSVLogger
import matplotlib.pyplot as mpl

from Predict import runModel

import LandmarkLogger as ll


# Reads points.txt, returns
    # array of tags (1 = focused, 0 = unfocused) and
    # 2d array of points [x, y, z]
def getData(filename):
    with open(filename, 'r') as file:
        # Load all data
        data = file.readlines()
        data = ''.join(data).split('\n')
        temp = []
        for item in data:
            if item != '':
                temp.append(item)
        data = temp

        # Extract tags and points
        tags, points = [], []
        for item in data[1:]:
            tags.append(int(item[0]))
            points.append(item[2:])

        # Convert to 1d vectors
        for i, point in enumerate(points):
            points[i] = [float(num) for num in point.split()]

    return tags, points

# Trains nerualnet, saves at path
def trainNN(tagsIn, pointsIn, modelPath, epochs):
    perm = np.random.permutation(len(tagsIn))

    pointsPerSample = len(pointsIn[0])

    splitInd = int(0.8 * len(pointsIn))
    pointsTrain, tagsTrain = pointsIn[:splitInd], tagsIn[:splitInd]
    pointsTest, tagsTest = pointsIn[splitInd:], tagsIn[splitInd:]

    checkpoint_callback = ModelCheckpoint('model_weights.h5', monitor='val_accuracy', save_best_only=True,
                                          save_weights_only=True, mode='max', verbose=1)
    csv_logger = CSVLogger('training.log', separator=',', append=False)


    # Building the model
    model = Sequential([])

    # Hidden layers
    # model.add(layers.Dense(units = 64, input_dim=len(pointsIn[0]), activation= 'relu')) # tune
    # model.add(layers.Dropout(0.5)) # tune
    # model.add(layers.Dense(units=32, activation='relu')) # tune
    model.add(layers.Dense(units=32, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(units=32, activation='relu'))

    # Output layers
    model.add(layers.Dense(units=1, activation = 'sigmoid'))

    # Training
    # model.compile(optimizer = Adam(learning_rate = 0.001), loss = 'binary_crossentropy', metrics = ['accuracy']) # tune;
    model.compile(optimizer=Adam(learning_rate=0.0003), loss='binary_crossentropy', metrics=['accuracy'])
    print('Training model...')
    trainingLog = model.fit(pointsTrain, tagsTrain, epochs = epochs, batch_size = 64, validation_data = (pointsTest, tagsTest)) # tune
    model.save(modelPath)

    valAccData = np.array(trainingLog.history['val_accuracy'])
    trainAccData = np.array(trainingLog.history['accuracy'])

    return valAccData, trainAccData






if __name__ == '__main__':
    # ll.setWantedPoints(False, 30/60, 30, None)

    tags, points = getData('points.txt')

    valAccData, trainAccData = trainNN(tags, points, 'model.h5', 30)

    mpl.plot(valAccData)
    mpl.plot(trainAccData)
    mpl.show()

    # runModel(None)














