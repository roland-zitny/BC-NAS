import os
import pickle
import nas.main as main_file
from PyQt5.QtGui import QPixmap
import cv2
from PIL import Image
import io
import base64


class User:
    """
        Class for saving and loading user data.

        Attributes
        ----------
        name: string
            name of user

        surname: string
            surname of user

        login_name: string
            ID of user used for login.

        Methods
        -------
        set_user_stimulus():
            stimulus setter.

        get_user_stimulus():
            stimulus getter.

        set_test_data():
            test data setter.

        get_test_data():
            test data getter.

        save_user():
            Pickle user.

    """

    def __init__(self, name, surname, login_name):
        self.login_name = login_name
        self.name = name
        self.surname = surname
        self.stimulus_b64 = None
        self.user_epochs = None
        self.epochs_types = None

    def set_user_stimulus(self, stimulus):
        """
            Stimulus setter

            :param XXX: neviem
        """

        self.stimulus_b64 = stimulus

    def get_user_stimulus(self):
        """
            Stimulus getter.
        """

        return self.stimulus_b64

    def set_test_data(self, epochs, epochs_types):
        """
            Test data setter.
        """

        self.user_epochs = epochs
        self.epochs_types = epochs_types

    def get_test_data(self):
        """
            Test data getter.
        """

        return self.user_epochs, self.epochs_types

    def save_user(self):
        """
            Method to save user object as pickle.
        """

        path = os.path.join(os.path.dirname(main_file.__file__), "db", self.login_name + ".p")
        pickle.dump(self, open(path, "wb"))

    def print_data(self):
        print("USER PRINT DATA")
        print(self.login_name)
        print(self.name)
        print(self.surname)
        print(self.epochs_types)
        print(self.user_epochs)
