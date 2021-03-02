import cv2
import base64
import os
import nas.main as main_file


class StimuliCreator(object):
    """
        Class used to obtain stimulus from image of user.
        Stimulus is image saved encoded as base64.

        Attributes
        ----------
        path : str
            path to image

        Methods
        -------
        create()
            Creates and set stimulus.

        get_status()
            Gets status of operation for error handling.

        get_face_b64()
            Get image encoded as base64.
    """

    def __init__(self, path):
        self.image_path = path
        self.face_b64 = None
        self.status = False
        self.create()

    # noinspection PyBroadException
    def create(self):
        """
            Find face in image and save it.
        """

        tmp_image_path = os.path.join(os.path.dirname(main_file.__file__), "db", "tmp", 'processed_photo.jpg')

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
            Get status of operation.
        """
        return self.status

    def get_face_b64(self):
        """
            Get image encoded as base64.
        """
        return self.face_b64
