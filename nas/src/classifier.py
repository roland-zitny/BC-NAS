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
            model.fit(self.fit_data, self.reg_data_types)
            self.predict_data = self.predict_data
            result = model.predict(self.predict_data)
            return result

        if classification_method == "CNN":
            num_of_x = round(BoardShim.get_sampling_rate(config.BOARD_TYPE) * 0.6)

            #model = models.Sequential()
            #model.add(layers.Conv2D(5, (4, 1), activation='relu', input_shape=(50, 4, 150, 1)))
            #model.add(layers.Flatten())
            #model.add(layers.Dense(2))
            #model.summary()

            #model.compile(optimizer='adam',
            #              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            #              metrics=['accuracy'])

            #x = self.reg_data
            #input_d = np.array(self.reg_data)
            #output_d = self.reg_data_types

            #model.fit(input_d, output_d, epochs=1)
            ################################################################
            ######################## 1D ####################################

            # cim mensi filter shape tym mensie featury hlada , asi mensie filtre su lepsie. Najcastejsie pouzivany
            # filte je 3x3

            input_shape = (50, 4, 150)
            model = models.Sequential()

            model.add(layers.Conv1D(32, 1, activation='relu', input_shape=input_shape[1:]))
            model.add(layers.MaxPooling1D(pool_size=2))

            model.add(layers.Conv1D(64, 1, activation='relu'))
            model.add(layers.MaxPooling1D(pool_size=2))

            model.add(layers.Flatten())

            model.add(layers.Dense(128, activation='relu'))
            model.add(layers.Dense(2, activation='relu'))

            model.summary()

            model.compile(optimizer='adam',
                          loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                          metrics=['accuracy'])

            x = self.reg_data
            input_d = np.array(self.reg_data)
            output_d = self.reg_data_types
            model.fit(input_d, output_d, epochs=1)

            info = model.predict(input_d).astype("int32")

            print(info)

            return [0, 1, 2, 3]
