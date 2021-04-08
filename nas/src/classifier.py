import os
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

        self.result = None

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
            model = LinearDiscriminantAnalysis()
            model.fit(self.fit_data, self.reg_data_types)
            self.result = model.predict(self.predict_data)

        if classification_method == "CNN":
            restored_data = DataFilter.read_file('5a.csv')
            data = [restored_data[10][:-18], restored_data[11][:-18], restored_data[2][:-18], restored_data[3][:-18]]

            # DATA
            #10,11,2,3
            #168 samples
            data_0 = np.split(data[0], 50)
            data_1 = np.split(data[1], 50)
            data_2 = np.split(data[2], 50)
            data_3 = np.split(data[3], 50)

            training_labels = [0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1
                               ,0,0,0,0,1,0,0,0,0,1]

            training_samples = []

            scaler = MinMaxScaler(feature_range=(0, 1))
            training_labels = np.array(training_labels)
            x = scaler.fit_transform(training_labels.reshape(-1, 1))

            for i in range(len(data_0)):
                window1 = np.array(data_0[i])
                window1 = scaler.fit_transform(window1.reshape(-1, 1))
                window2 = np.array(data_1[i])
                window2 = scaler.fit_transform(window2.reshape(-1, 1))
                window3 = np.array(data_2[i])
                window3 = scaler.fit_transform(window3.reshape(-1, 1))
                window4 = np.array(data_3[i])
                window4 = scaler.fit_transform(window4.reshape(-1, 1))

                window = [window1,window2,window3,window4]

                training_samples.append(window)

            # Change data to numpy array
            # 1,4,168
            training_labels = np.array(training_labels)
            training_samples = np.array(training_samples)

            training_labels, training_samples = shuffle(training_labels, training_samples)

            # MODEL
            model = models.Sequential([
                layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same',
                              input_shape=(4, 168, 1)),
                layers.MaxPooling2D(pool_size=(1, 2), strides=2),
                layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'),
                layers.MaxPooling2D(pool_size=(1, 2), strides=2),
                layers.Flatten(),
                layers.Dense(units=2, activation='softmax'),
            ])

            model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy',
                          metrics=['accuracy'])

            model.fit(x=training_samples,
                      y=training_labels,
                      validation_split=0.2,
                      batch_size=1,
                      epochs=400,
                      shuffle=True,
                      verbose=2)

    def determine_access_right(self):
        #TODO
        self.login_data_types = self.reg_data_types

        print(self.login_data_types)
        print(self.result)

        correct_reactions = 0

        for i in range(len(self.login_data_types)):
            if self.login_data_types[i] == self.result[i]:
                correct_reactions += 1

        print(correct_reactions)
        return 1

