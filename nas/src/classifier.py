import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


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
