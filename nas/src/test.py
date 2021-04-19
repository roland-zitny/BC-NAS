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

file = "test_stare.p"
FILE = os.path.join(os.path.dirname(main_file.__file__), "datasets", file)  # DB directory path.

if __name__ == '__main__':
    pickle_file = open(FILE, 'rb')
    dataset = pickle.load(pickle_file)
    pickle_file.close()
    reg_data, reg_data_types, login_data, login_data_types = dataset.get_dataset()

    ################# LDA #################################
    #for i in range(len(reg_data)):
    #    plt.figure(i)
    #    plt.plot(login_data[i][3])
    #    plt.show()

    fit_data = []
    fit_data_types = []
    predict_data = []
    predict_data_types = []

    for i in range(len(reg_data)):
        epoch = np.array([])
        for y in range(len(reg_data[i])):
            norm_data = preprocessing.normalize(np.array([reg_data[i][y]]))
            epoch = np.concatenate((epoch, norm_data[0]))

        fit_data.append(epoch)
        fit_data_types.append(reg_data_types[i])

    for i in range(len(login_data)):
        epoch = np.array([])
        for y in range(len(login_data[i])):
            norm_data = preprocessing.normalize(np.array([login_data[i][y]]))
            epoch = np.concatenate((epoch, norm_data[0]))

        predict_data.append(epoch)
        predict_data_types.append(login_data_types[i])


    ##############################################################
    model = LinearDiscriminantAnalysis()
    model.fit(fit_data, fit_data_types)
    result = model.predict(predict_data)

    print(predict_data_types)
    print(result)
    ############################### ROC AUC ######################
    fpr_rf, tpr_rf, thresholds_rf = roc_curve(predict_data_types, result)
    auc_rf = auc(fpr_rf, tpr_rf)

    fig = plt.figure(1)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr_rf, tpr_rf, label='LDA (area = {:.3f})'.format(auc_rf))
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