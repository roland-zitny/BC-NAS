import base64
import os
import random
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QImage
from nas.src import config


class StimuliCreator:
    """
        Class for random display of stimuli to the user.
        These stimuli consist of `self-face` and `non-self-face` images.

        :param user_face: User stimulus.
        :type user_face: base64 string
    """

    def __init__(self, user_face):
        self.user_face = user_face
        self.stimuli_types = np.array([])
        self.self_face_count = 0
        self.non_self_face_count = 0
        self.pause_sequence = 0
        self.pause_offset = 0

    def learning_stimuli(self):
        """
            Stimulation for the registration process.
            This stimulation is not randomized.
            Every fifth stimulus is self-face stimulus.

            :return: ``set_non_self_face_stimulus()`` or ``set_self_face_stimulus()``
            :rtype: QPixmap
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
            return self.set_non_self_face_stimulus()

    def randomized_stimuli(self):
        """
            Stimulation for the log in process.
            This stimulation is randomized.

            :return: ``set_non_self_face_stimulus()`` or ``set_self_face_stimulus()``
            :rtype: QPixmap
        """

        if self.self_face_count < round(config.STIMULI_NUM * 0.2):
            if self.pause_sequence == 0:
                self.pause_sequence = random.randint(1, 4)

            if self.non_self_face_count < (self.pause_sequence + self.pause_offset):
                self.non_self_face_count += 1
                self.stimuli_types = np.append(self.stimuli_types, 0)
                return self.set_non_self_face_stimulus()
            else:
                self.self_face_count += 1
                self.non_self_face_count = 0
                self.pause_offset = 4 - self.pause_sequence
                self.pause_sequence = 0
                self.stimuli_types = np.append(self.stimuli_types, 1)
                return self.set_self_face_stimulus()
        else:
            self.stimuli_types = np.append(self.stimuli_types, 0)
            return self.set_non_self_face_stimulus()

    @staticmethod
    def set_non_self_face_stimulus():
        """
             Get non-self-face stimulus.

             :return: Specific non-self-face stimulus.
             :rtype: QPixmap
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
             Get self-face stimulus.

             :return: Self-face stimulus.
             :rtype: QPixmap
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
            Return types of generated stimuli types.
            This list is used for classification.

            :return: List of generated stimuli types.
            :rtype: list
        """

        # Need to remove last types because we show one more stimulus just for time synch.
        return self.stimuli_types[:-1]
