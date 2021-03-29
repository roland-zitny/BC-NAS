import numpy as np
import matplotlib.pyplot as plt
from brainflow import DataFilter
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from brainflow import BoardShim, BoardIds, DataFilter, AggOperations, FilterTypes


# KLASIFIKACIA


class Classifier:
    def __init__(self, login_data, reg_data, reg_data_types):
        self.login_data = login_data
        self.reg_data = reg_data
        self.reg_data_types = reg_data_types
        self.fit_data = []
        self.predict_data = []

    def reduce_dimension_lda(self):

        #INTEGRAL TODO
        #x = scipy.integrate.simps((stimuli_epochs[0])[0])

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

    def classifie(self, type):
        if type == "LDA":
            print("LDA")
            self.fit_data = self.fit_data[:-1]
            self.reg_data_types = self.reg_data_types[:-1]
            model = LinearDiscriminantAnalysis()
            model.fit(self.fit_data, self.reg_data_types)
            self.predict_data = self.predict_data[:-1]
            result = model.predict(self.predict_data)
            return result