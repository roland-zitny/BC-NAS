import os

import scipy
from sklearn import preprocessing
from sklearn.covariance import OAS

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from tensorflow.keras import layers, models
from nas.src import config
from brainflow import BoardShim
from tensorflow.keras.optimizers import Adam


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

    def __init__(self, login_data, reg_data, reg_data_types, login_data_types, user_ids=None):
        self.login_data = login_data
        self.reg_data = reg_data
        self.reg_data_types = reg_data_types
        self.login_data_types = login_data_types
        self.user_ids = user_ids

        # LDA input
        self.fit_data = []
        self.predict_data = []
        self.fit_data_types = []
        self.predict_data_types = []

        # CNN input
        self.training_samples = None
        self.predicting_samples = None
        self.training_samples_types = []
        self.predicting_samples_types = []

        # Result
        self.result = None

    def prepare_cnn_data(self):
        """
            Data preparation for CNN.
        """

        training_samples = []
        predicting_samples = []
        predict_data_types = []
        training_data_types = []

        for i in range(len(self.reg_data)):
            epoch = []
            norm_data_0 = preprocessing.normalize(np.array([self.reg_data[i][0]]))
            norm_data_1 = preprocessing.normalize(np.array([self.reg_data[i][1]]))
            norm_data_2 = preprocessing.normalize(np.array([self.reg_data[i][2]]))
            norm_data_3 = preprocessing.normalize(np.array([self.reg_data[i][3]]))
            epoch = np.array([[norm_data_0[0], norm_data_1[0], norm_data_2[0], norm_data_3[0]]])
            training_samples.append(epoch)
            training_data_types.append(self.reg_data_types[i])

        for i in range(len(self.login_data)):
            epoch = []
            norm_data_0 = preprocessing.normalize(np.array([self.login_data[i][0]]))
            norm_data_1 = preprocessing.normalize(np.array([self.login_data[i][1]]))
            norm_data_2 = preprocessing.normalize(np.array([self.login_data[i][2]]))
            norm_data_3 = preprocessing.normalize(np.array([self.login_data[i][3]]))
            epoch = np.array([[norm_data_0[0], norm_data_1[0], norm_data_2[0], norm_data_3[0]]])
            predicting_samples.append(epoch)
            predict_data_types.append(self.login_data_types[i])

        training_samples = np.array(training_samples)
        predicting_samples = np.array(predicting_samples)
        training_data_types = np.array(training_data_types)
        predict_data_types = np.array(predict_data_types)

        num_of_x = round(BoardShim.get_sampling_rate(config.BOARD_TYPE) * 0.8)
        training_samples = training_samples.reshape(len(training_samples), 4, num_of_x, 1)
        predicting_samples = predicting_samples.reshape(len(predicting_samples), 4, num_of_x, 1)

        self.training_samples = training_samples
        self.training_samples_types = training_data_types
        self.predicting_samples = predicting_samples
        self.predicting_samples_types = predict_data_types

    def classify(self, classification_method):
        """
            Classify login EEG data.

            :param classification_method: Method of classification.
            :type classification_method: string
            :return: Result of classification.
            :rtype: list
        """

        if classification_method == "LDA" or classification_method == "BOTH":
            model = LinearDiscriminantAnalysis(solver='lsqr', shrinkage=0.924)
            model.fit(self.fit_data, self.fit_data_types)

            self.result = model.predict(self.predict_data)

        if classification_method == "CNN" or classification_method == "BOTH":
            num_of_x = round(BoardShim.get_sampling_rate(config.BOARD_TYPE) * 0.8)

            model = models.Sequential([
                layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same',
                              input_shape=(4, num_of_x, 1), use_bias=True),
                layers.MaxPooling2D(pool_size=(1, 4), strides=1),

                layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same', use_bias=True),
                layers.MaxPooling2D(pool_size=(1, 4), strides=1),

                layers.Flatten(),
                layers.Dense(units=500, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.2),
                layers.Dense(units=100, activation='relu'),
                layers.Dense(units=2, activation='softmax'),
            ])

            model.compile(optimizer=Adam(learning_rate=0.002), loss='sparse_categorical_crossentropy',
                          metrics=['accuracy'])

            model.fit(x=self.training_samples,
                      y=self.reg_data_types,
                      batch_size=10,
                      epochs=30,
                      verbose=0,
                      shuffle=True)

            result = model.predict(x=self.predicting_samples, batch_size=1, verbose=0)
            result = np.round(result)
            result = result[:, 0]
            self.result = result

    def prepare_lda_data(self):
        """
            Data preparation for LDA.
        """

        fit_data = []
        fit_data_types = []
        predict_data = []
        predict_data_types = []

        for i in range(len(self.reg_data)):
            epoch = []
            norm_data_0 = preprocessing.normalize(np.array([self.reg_data[i][0]]))
            norm_data_1 = preprocessing.normalize(np.array([self.reg_data[i][1]]))
            norm_data_2 = preprocessing.normalize(np.array([self.reg_data[i][2]]))
            norm_data_3 = preprocessing.normalize(np.array([self.reg_data[i][3]]))

            avg = (norm_data_0 + norm_data_1 + norm_data_2 + norm_data_3) / 4
            epoch = avg[0]
            fit_data.append(epoch)

        for i in range(len(self.login_data)):
            epoch = []
            norm_data_0 = preprocessing.normalize(np.array([self.login_data[i][0]]))
            norm_data_1 = preprocessing.normalize(np.array([self.login_data[i][1]]))
            norm_data_2 = preprocessing.normalize(np.array([self.login_data[i][2]]))
            norm_data_3 = preprocessing.normalize(np.array([self.login_data[i][3]]))

            avg = (norm_data_0 + norm_data_1 + norm_data_2 + norm_data_3) / 4
            epoch = avg[0]
            predict_data.append(epoch)

        fit_data = np.array(fit_data)
        fit_data_types = self.reg_data_types
        predict_data = np.array(predict_data)
        predict_data_types = self.login_data_types

        self.fit_data = fit_data
        self.fit_data_types = fit_data_types
        self.predict_data = predict_data
        self.predict_data_types = predict_data_types

    def identification(self, classification_method):
        """
             Classification of reactions in the identification process.
        """

        model = LinearDiscriminantAnalysis(solver='lsqr', shrinkage=0.924)
        model.fit(self.fit_data, self.fit_data_types)
        result = model.predict(self.predict_data)

        self.result = result

    def determine_user_id(self):
        """
            This method determines the user ID.
        """

        pos_reactions = []

        for i in range(len(self.result)):
            if self.result[i] == 1:
                pos_reactions.append(self.login_data_types[i])

        try:
            predicted_id = max(set(pos_reactions), key=pos_reactions.count)
            return predicted_id
        except:
            return None

    def determine_access_right(self):
        """
            This method determines the result of the user's login.

            :return True or False
        """

        correct_self_face_reactions = 0
        correct_non_self_face_reactions = 0

        for i in range(len(self.login_data_types)):
            if self.login_data_types[i] == 1 and self.login_data_types[i] == self.result[i]:
                correct_self_face_reactions += 1
            if self.login_data_types[i] == 0 and self.login_data_types[i] == self.result[i]:
                correct_non_self_face_reactions += 1

        self_face_accuracy = (100 / round(config.STIMULI_NUM * 0.2) * correct_self_face_reactions)
        non_self_face_accuracy = (100 / config.STIMULI_NUM * correct_non_self_face_reactions)

        if self_face_accuracy >= 40 and non_self_face_accuracy >= 60:
            return True
        else:
            return False
