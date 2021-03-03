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

    def save_pickle(self):
        ###########################################################
        #with open("processed_face.jpg", "rb") as img_file:
        #    my_string = base64.b64encode(img_file.read())

        #with open("imageToSave.png", "wb") as fh:
        #    fh.write(base64.decodebytes(my_string))
        pass

    def b64tocv2(self):
        # im_bytes = base64.b64decode(im_b64)
        # im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        # img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        pass

    def print_name(self):
        print(self.name)
