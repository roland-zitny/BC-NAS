import cv2
import base64
from nas.src import config


class SelfFace(object):
    """
        A class that creates a stimulus from a photo of a user's face.
        Stimulus is an image encoded in base64 string.

        :param path: Path to the desired photo. This path can be changed in ``config.py``.
        :type path: string
    """

    def __init__(self, path):
        self.image_path = path
        self.face_b64 = None
        self.status = False
        self.create()

    # noinspection PyBroadException
    def create(self):
        """
            It will try to crop the user's face.
            Sets the success of the operation.
            Sets the success of the operation and encodes this result using `base64`.
            The processed photo is temporarily saved in `tmp_image_path`.
            This path can be changed in ``config.py``.
        """

        tmp_image_path = config.TMP_PROC_PHOTO

        try:
            image = cv2.imread(self.image_path)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(image, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                faces = image[y:y + h, x:x + w]

            cv2.imwrite(tmp_image_path, faces)

            img = cv2.imread(tmp_image_path)
            _, im_arr = cv2.imencode('.jpg', img)
            im_bytes = im_arr.tobytes()
            im_b64 = base64.b64encode(im_bytes)
            self.face_b64 = im_b64
            self.status = True
        except:
            self.status = False

    def get_status(self):
        """
            `Create` status getter.
            This status is used to report an error to the user.

            :return: Status of operation. ``True`` if successful otherwise ``False``.
            :rtype: bool
        """

        return self.status

    def get_face_b64(self):
        """
            Stimulus getter.

            :return: Encoded stimulus.
            :rtype: base64 string
        """
        return self.face_b64
