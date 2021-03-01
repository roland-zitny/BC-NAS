from PyQt5.QtGui import QPixmap
import cv2
from PIL import Image
import io
import base64

class User:
    def __init__(self, name, surname):
        print("MAME USERA")
        self.name = name

    def save_pickle(self):
        ###########################################################
        #with open("processed_face.jpg", "rb") as img_file:
        #    my_string = base64.b64encode(img_file.read())

        #with open("imageToSave.png", "wb") as fh:
        #    fh.write(base64.decodebytes(my_string))
        pass

    def print_name(self):
        print(self.name)
