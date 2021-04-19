import os

import scipy
from sklearn import preprocessing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from brainflow import BoardShim, DataFilter, FilterTypes, AggOperations
import tensorflow as tf
from tensorflow.keras import layers, models
from nas.src import config
from brainflow import BoardShim
from brainflow.data_filter import DataFilter
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.optimizers import Adam
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import matplotlib.pyplot as plt
import nas.main as main_file
from nas.src.dataset import Dataset
import time

import os
import pickle
import matplotlib.pyplot as plt
#from nas.src.classifier import Classifier
from brainflow.board_shim import BoardIds
import nas.main as main_file
import numpy as np


file = "5b.p"
FILE = os.path.join(os.path.dirname(main_file.__file__), "datasets", file)  # DB directory path.

restored_data = DataFilter.read_file('test.csv')


if __name__ == '__main__':
    pickle_file = open(FILE, 'rb')
    dataset = pickle.load(pickle_file)
    pickle_file.close()
    reg_data, reg_data_types, login_data, login_data_types = dataset.get_dataset()

    ################################################################################################
    training_samples = None
    predicting_samples = None

    result = None

    scaler = MinMaxScaler(feature_range=(0, 1))
    training_samples = []
    predicting_samples = []
    predict_data_types = []
    training_data_types = []

    for i in range(len(reg_data)):
        wind_0 = reg_data[i][0].reshape(-1, 1)
        wind_1 = reg_data[i][1].reshape(-1, 1)
        wind_2 = reg_data[i][2].reshape(-1, 1)
        wind_3 = reg_data[i][3].reshape(-1, 1)
        window = [wind_0, wind_1, wind_2, wind_3]
        training_samples.append(window)
        training_data_types.append(reg_data_types[i])

    for i in range(len(login_data)):
        wind_0 = login_data[i][0].reshape(-1, 1)
        wind_1 = login_data[i][1].reshape(-1, 1)
        wind_2 = login_data[i][2].reshape(-1, 1)
        wind_3 = login_data[i][3].reshape(-1, 1)
        window = [wind_0, wind_1, wind_2, wind_3]
        predicting_samples.append(window)
        predict_data_types.append(login_data_types[i])


    # change on numpy array
    training_samples = np.array(training_samples)
    predicting_samples = np.array(predicting_samples)
    training_data_types = np.array(training_data_types)
    predict_data_types = np.array(predict_data_types)

    ########################## MODEL ###############################################################
    num_of_x = 75
    model = models.Sequential([
        layers.Conv2D(filters=6, kernel_size=(3, 3), activation='elu', input_shape=(4, num_of_x, 1)),
        layers.BatchNormalization(),
        #layers.Dropout(0.5),
        layers.AveragePooling2D(pool_size=(1, 4)),
        layers.Flatten(),
        layers.Dense(100, activation='elu'),
        layers.BatchNormalization(),
        #layers.Dropout(0.5),
        layers.Dense(2, activation='softmax'),
    ])

    model.summary()
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])  # ROC AUC

    model.fit(x=training_samples,
              y=training_data_types,
              batch_size=4,
              epochs=1000,
              verbose=2,
              shuffle=True)

    result = model.predict(x=predicting_samples)
    result = np.round(result)
    result = result[:, 0]

    ############################### ROC AUC ######################
    fpr_rf, tpr_rf, thresholds_rf = roc_curve(predict_data_types, result)
    auc_rf = auc(fpr_rf, tpr_rf)

    fig = plt.figure(1)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr_rf, tpr_rf, label='CNN (area = {:.3f})'.format(auc_rf))
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='best')
    plt.show()

    correct_self_face_reactions = 0
    correct_non_self_face_reactions = 0

    for i in range(len(login_data_types)):
        if login_data_types[i] == 1 and login_data_types[i] == result[i]:
            correct_self_face_reactions += 1
        if login_data_types[i] == 0 and login_data_types[i] == result[i]:
            correct_non_self_face_reactions += 1

    print(correct_self_face_reactions)
    print(correct_non_self_face_reactions)