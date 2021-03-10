import os
import pickle
import nas.main as main_file
from PyQt5.QtGui import QPixmap
import cv2
from PIL import Image
import io
import base64


class User:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.stimulus_b64 = None

    def set_user_stimulus(self, stimulus):
        self.stimulus_b64 = stimulus

    def get_user_stimulus(self):
        return self.stimulus_b64

    def save_user(self):
        path = os.path.join(os.path.dirname(main_file.__file__), "db", self.name + "_" + self.surname + ".p")
        pickle.dump(self, open(path, "wb"))

    def print_data(self):
        print(self.name)
        print(self.surname)
