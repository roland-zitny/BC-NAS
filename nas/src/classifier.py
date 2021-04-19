import os

import scipy
from sklearn import preprocessing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
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


class Classifier:
    """
        A class that classifies login EEG data.

        :param login_data: Login EEG data. List of login data time windows.
        :type login_data: list

        :param reg_data: Registration EEG data. List of registration data time windows.
        :type reg_data: list

        :param reg_data_types: Registration data time windows types.
        :type reg_data_types: list
    """

    def __init__(self, login_data, reg_data, reg_data_types, login_data_types):
        self.login_data = login_data
        self.reg_data = reg_data
        self.reg_data_types = reg_data_types
        self.login_data_types = login_data_types

        # Reduced data.
        self.fit_data = []
        self.predict_data = []

        self.training_samples = None
        self.predicting_samples = None

        self.result = None

    def reduce_dimension_lda(self):
        """
            Reduction of the dimension of EEG data for the correct functioning of the classification method.
        """

        # INTEGRAL TODO
        neviem = scipy.integrate.simps((self.login_data[0][0]))
        print(neviem)

        scaler = MinMaxScaler(feature_range=(0, 1))

        for i in range(len(self.reg_data)):
            epoch = np.array([])
            for y in range(len(self.reg_data[i])):
                epoch = np.concatenate((epoch, self.reg_data[i][y]))

            self.fit_data.append(epoch)

        for i in range(len(self.login_data)):
            epoch = np.array([])
            for y in range(len(self.login_data[i])):
                epoch = np.concatenate((epoch, self.login_data[i][y]))

            self.predict_data.append(epoch)

    def prepare_cnn_data(self):
        scaler = MinMaxScaler(feature_range=(0, 1))
        training_samples = []

        for i in range(len(self.reg_data)):
            #wind_0 = scaler.fit_transform(self.reg_data[i][0].reshape(-1, 1))
            wind_0 = self.reg_data[i][0].reshape(-1, 1)
            #wind_1 = scaler.fit_transform(self.reg_data[i][1].reshape(-1, 1))
            wind_1 = self.reg_data[i][1].reshape(-1, 1)
            #wind_2 = scaler.fit_transform(self.reg_data[i][2].reshape(-1, 1))
            wind_2 = self.reg_data[i][2].reshape(-1, 1)
            #wind_3 = scaler.fit_transform(self.reg_data[i][3].reshape(-1, 1))
            wind_3 = self.reg_data[i][3].reshape(-1, 1)
            window = [wind_0, wind_1, wind_2, wind_3]
            training_samples.append(window)

        self.training_samples = np.array(training_samples)

        predicting_samples = []

        for i in range(len(self.login_data)):
            wind_0 = scaler.fit_transform(self.login_data[i][0].reshape(-1, 1))
            wind_1 = scaler.fit_transform(self.login_data[i][1].reshape(-1, 1))
            wind_2 = scaler.fit_transform(self.login_data[i][2].reshape(-1, 1))
            wind_3 = scaler.fit_transform(self.login_data[i][3].reshape(-1, 1))
            window = [wind_0, wind_1, wind_2, wind_3]
            predicting_samples.append(window)

        self.predicting_samples = np.array(predicting_samples)

    def classify(self, classification_method):
        """
            Classify login EEG data.

            :param classification_method: Method of classification.
            :type classification_method: string
            :return: Result of classification.
            :rtype: list
        """
        # TODO normalizacia taktato
        # scaler = MinMaxScaler(feature_range=(0,1))
        # scaled_train_samples = scaler.fit_transform(train_samples.reshape(-1,1))
        if classification_method == "LDA" or classification_method == "BOTH":
            model = LinearDiscriminantAnalysis()
            model.fit(self.fit_data, self.reg_data_types)
            self.result = model.predict(self.predict_data)

            print(self.login_data_types)
            print(self.result)

            print("LDA HORE")

            fpr_rf, tpr_rf, thresholds_rf = roc_curve(self.login_data_types, self.result)
            auc_rf = auc(fpr_rf, tpr_rf)

        if classification_method == "CNN" or classification_method == "BOTH":
            # MODEL
            # input data of board
            num_of_x = round(BoardShim.get_sampling_rate(config.BOARD_TYPE) * 0.8)

            model = models.Sequential([
                layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same',
                              input_shape=(4, num_of_x, 1)),
                layers.MaxPooling2D(pool_size=(1, 2), strides=2),
                layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'),
                layers.MaxPooling2D(pool_size=(1, 2), strides=2),
                layers.Flatten(),
                layers.Dense(units=2, activation='softmax'),
            ])

            model.summary()
            model.compile(optimizer=Adam(learning_rate=0.0003), loss='sparse_categorical_crossentropy',
                          metrics=['accuracy'])     # ROC AUC

            model.fit(x=self.training_samples,
                      y=self.reg_data_types,
                      batch_size=1,
                      epochs=500,
                      verbose=2)

            result = model.predict(x=self.predicting_samples)
            print("RESULT NESPRACOVANE")
            print(result)
            result = np.round(result)
            result = result[:,0]
            self.result = result

        fpr_keras, tpr_keras, thresholds_keras = roc_curve(self.login_data_types, self.result)
        auc_keras = auc(fpr_keras, tpr_keras)

        fig = plt.figure(1500)
        plt.plot([0, 1], [0, 1], 'k--')

        if classification_method == "CNN" or classification_method == "BOTH":
            plt.plot(fpr_keras, tpr_keras, label='CNN (area = {:.3f})'.format(auc_keras))
        if classification_method == "LDA" or classification_method == "BOTH":
            plt.plot(fpr_rf, tpr_rf, label='LDA (area = {:.3f})'.format(auc_rf))

        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.title('ROC curve')
        plt.legend(loc='best')
        ts = time.time()
        plt.savefig(os.path.join(os.path.dirname(main_file.__file__), "datasets", str(ts) + ".jpg"))
        fig

        plt.show()

        dataset = Dataset(self.reg_data, self.reg_data_types, self.login_data, self.login_data_types)
        dataset.save_dataset()

    def determine_access_right(self):
        print(self.login_data_types)
        print(self.result)

        correct_self_face_reactions = 0
        correct_non_self_face_reactions = 0

        for i in range(len(self.login_data_types)):
            if self.login_data_types[i] == 1 and self.login_data_types[i] == self.result[i]:
                correct_self_face_reactions += 1
            if self.login_data_types[i] == 0 and self.login_data_types[i] == self.result[i]:
                correct_non_self_face_reactions += 1

        print(correct_self_face_reactions)
        print(correct_non_self_face_reactions)

        self_face_accuracy = (100 / round(config.STIMULI_NUM*0.2) * correct_self_face_reactions)
        non_self_face_accuracy = (100 / config.STIMULI_NUM * correct_non_self_face_reactions)

        if self_face_accuracy >= 70 and non_self_face_accuracy >= 60:
            return True
        else:
            return False

