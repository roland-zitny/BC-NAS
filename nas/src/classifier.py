import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from nas.src import config
from brainflow import BoardShim

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

    def __init__(self, login_data, reg_data, reg_data_types):
        self.login_data = login_data
        self.reg_data = reg_data
        self.reg_data_types = reg_data_types
        self.fit_data = []
        self.predict_data = []

    def reduce_dimension_lda(self):
        """
            Reduction of the dimension of EEG data for the correct functioning of the classification method.
        """

        # INTEGRAL TODO
        # x = scipy.integrate.simps((stimuli_epochs[0])[0])

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

    def classify(self, classification_method):
        """
            Classify login EEG data.

            :param classification_method: Method of classification.
            :type classification_method: string
            :return: Result of classification.
            :rtype: list
        """

        if classification_method == "LDA":
            self.fit_data = self.fit_data
            self.reg_data_types = self.reg_data_types
            model = LinearDiscriminantAnalysis()
            model.fit(self.fit_data, self.reg_data_types[:-1])
            self.predict_data = self.predict_data
            result = model.predict(self.predict_data)
            return result

        if classification_method == "CNN":
            num_of_x = round(BoardShim.get_sampling_rate(config.BOARD_TYPE) * 0.6)

            model = models.Sequential()
            model.add(layers.Conv1D(40, kernel_size=2, activation='relu', input_shape=(4,150)))
            model.add(layers.Flatten())
            model.add(layers.Dense(2))
            model.summary()

            model.compile(optimizer='adam',
                          loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                          metrics=['accuracy'])

            x = self.reg_data[0].tolist()
            x1 = self.reg_data[1].tolist()
            x2 = self.reg_data[2].tolist()
            x3 = self.reg_data[3].tolist()
            x4 = self.reg_data[4].tolist()
            model.fit([x, x1, x2, x3, x4], [0, 1, 0, 0, 1], epochs=1)

            info = model.predict([x,x1,x4,x2,x3]).astype("int32")

            print(info)

            return [0, 1, 2, 3]
