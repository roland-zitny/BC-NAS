import os
import os.path
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pylab as plt
from tensorflow.keras.models import load_model


if __name__ == '__main__':
    # https://www.youtube.com/watch?v=qFJeN9V1ZsI&t=1321s

    ### 1 Treba spravit batches alebo numpy array inputu, cize z EEG.
    train_labels = [0,0]
    train_samples = [[[[1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10]]],
                     [[[1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10]]]]

    train_labels = np.array(train_labels)
    train_samples = np.array(train_samples)


    print(train_labels.shape)
    print(train_samples.shape)

    ### MODEL
    model = models.Sequential([
        layers.Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same', input_shape=(1,4,10)),
        layers.MaxPooling2D(pool_size=(1,2), strides=2),
        layers.Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'),
        layers.MaxPooling2D(pool_size=(1,2), strides=2),
        layers.Flatten(),
        layers.Dense(units=2, activation='softmax'),
    ])

    model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=train_samples, y=train_labels)

    predicted = model.predict(x=train_samples, verbose=0)
    predicted = np.round(predicted)
    print(predicted)

    ###########
    # CONFUSION MATRIX FOR BC DOC on https://www.youtube.com/watch?v=qFJeN9V1ZsI&t=1321s