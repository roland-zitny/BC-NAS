import base64
import os
import random
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QImage
from nas.src import config


class StimuliCreator:
    """
        Class to mimic random stimulation of user with images of faces.

        Attributes
        ----------
        user_face: base64
            face of user

        Methods
        -------
        learning_stimuli():
            Set of stimuli for registration.

        set_non_self_face_stimulus():
            Set non self face as stimulus.

        set_self_face_stimulus():
            Set self face as stimulus.

        get_stimuli_types():
            Returns types of stimuli.

    """

    def __init__(self, user_face):
        self.user_face = user_face
        self.stimuli_types = np.array([])
        self.self_face_count = 0
        self.non_self_face_count = 0

    def learning_stimuli(self):
        """
            Registration stimulation.
        """

        if self.self_face_count < 10:
            if self.non_self_face_count < 4:
                self.non_self_face_count += 1
                self.stimuli_types = np.append(self.stimuli_types, 0)
                return self.set_non_self_face_stimulus()  # Non Self Face
            else:
                self.self_face_count += 1
                self.non_self_face_count = 0
                self.stimuli_types = np.append(self.stimuli_types, 1)
                return self.set_self_face_stimulus()  # Self Face
        else:
            return None

    def randomized_stimuli(self):
        if self.self_face_count < 10:
            print("ss")

    def set_non_self_face_stimulus(self):
        """
             Set non self face as stimulus.
        """

        # Get number of files with non self faces.
        path = config.NON_FACE_DIR
        path, dirs, files = next(os.walk(path))
        file_count = len(files)

        file_number = random.randint(1, file_count)

        nonself_face_path = os.path.join(path + os.sep + str(file_number) + ".jpg")
        pixmap = QPixmap(nonself_face_path)
        return pixmap

    def set_self_face_stimulus(self):
        """
            Set self face as stimulus.
        """

        # Get image from user and use it as pixmap.
        im_bytes = base64.b64decode(self.user_face)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        # READ B64 image as QImage and set it as pixmap on label
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap(q_img)
        return pixmap

    def get_stimuli_types(self):
        """
            Return types of stimuli.
        """
        return self.stimuli_types
