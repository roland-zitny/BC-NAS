import cv2
import os
import base64
import numpy as np
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtMultimedia
from PyQt5 import QtMultimediaWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLabel
from nas.src.self_face import SelfFace
from reg_stimulation_window import RegStimuliPresentation
from nas.src import config

directory_path = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(directory_path, "designs" + os.sep + "registration_window.ui")
Ui_RegWindow, QtBaseClass = uic.loadUiType(ui_path)      # Load .ui file.


class RegistrationWindow(QtWidgets.QMainWindow, Ui_RegWindow):
    """
        Class for displaying the registration window of the graphical user interface and its manipulation.
        The main function of this window is to get a photo of the user's face and turn it into a stimulus.
        There are two options for capturing a photo, one via the device's camera and the other via file upload.

        :param reg_user: The object of the registering user.
        :type reg_user: ``user``
    """

    def __init__(self, reg_user):
        QtWidgets.QMainWindow.__init__(self)
        Ui_RegWindow.__init__(self)
        self.setupUi(self)
        # Object of user created in main program.
        self.reg_user = reg_user
        # User image file path.
        self.file_path = None
        self.FacePictureLabel = None
        self.CameraInfoLabel = None
        self.CameraViewfinder = None
        self.camera = None
        self.CameraCapture = None
        self.stimuli_window = None
        self.available_cameras = QtMultimedia.QCameraInfo.availableCameras()    # all available cameras of device
        self.set_up_window()

        # FLAGS
        self.FLAG_connected_camera = False  # True-> camera is connected, False -> camera is not connected
        self.FLAG_file_type = 0             # 0 -> None, 1 -> camera photo, 2 -> file

    def set_up_window(self):
        """
            Makes other window settings, such as connecting buttons, etc.
        """

        # Center window to screen.
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Create new qt widgets.
        self.create_camera_widgets()

        # Hide unnecessary widgets.
        self.CameraMenuWidget.hide()
        self.FileMenuWidget.hide()
        self.ProcessPhotoBtn.hide()
        self.CameraErrorLabel.hide()
        self.ContinueRegBtn.hide()
        self.CameraConfirmLabel.hide()

        # Connect ui buttons to methods.
        self.CameraMenuBtn.clicked.connect(self.show_camera_menu)
        self.CamConnectBtn.clicked.connect(self.connect_camera)
        self.TakePhotoBtn.clicked.connect(self.capture_photo)
        self.ShowPhotoBtn.clicked.connect(self.show_photo)
        self.FileBtn.clicked.connect(self.show_file_menu)
        self.FileFindBtn.clicked.connect(self.find_file)
        self.ChooseFileBtn.clicked.connect(self.choose_file)
        self.ProcessPhotoBtn.clicked.connect(self.process_photo)
        self.ContinueRegBtn.clicked.connect(self.continue_registration)

    def create_camera_widgets(self):
        """
            Creates necessary widgets for camera layout.
            `QLabel` for image itself.
            `QLabel` for message about this window.
            `QCameraViewfinder` for camera.
        """

        # Label with face of user, used to confirm photo or file.
        self.FacePictureLabel = QLabel()
        self.FacePictureLabel.setAlignment(Qt.AlignCenter)
        self.CameraLayout.addWidget(self.FacePictureLabel)
        self.FacePictureLabel.hide()

        # Message to tell user why we need his photo and what to do. Displayed on CameraLayout.
        self.CameraInfoLabel = QLabel("Pre správnu funkčnosť aplikácie je potrebné zaznamenať vašu fotku tváre.\n"
                                      "Zvolte možnosť odfotenia alebo výberu súboru.\n\n"
                                      "Vzniknutá fotka bude po procese registrácie odstránená.", self)

        self.CameraInfoLabel.setStyleSheet("font: 12pt Bahnschrift SemiBold; color: white;")
        self.CameraInfoLabel.setAlignment(Qt.AlignCenter)
        self.CameraLayout.addWidget(self.CameraInfoLabel)
        self.CameraInfoLabel.show()

        # Camera viewfinder, used to show camera input.
        self.CameraViewfinder = QtMultimediaWidgets.QCameraViewfinder()
        self.CameraLayout.addWidget(self.CameraViewfinder)
        self.CameraViewfinder.hide()

    def show_camera_menu(self):
        """
            Displays camera menu and all functional cameras.
            After choosing specific camera, it needs to be connected and controlled.
        """

        # Reset file type
        self.FLAG_file_type = 0

        # Show or hide widgets from CameraLayout.
        self.FacePictureLabel.hide()
        self.CameraViewfinder.hide()
        self.CameraInfoLabel.show()
        self.CameraErrorLabel.hide()
        self.ContinueRegBtn.hide()
        self.CameraConfirmLabel.hide()

        # Show or hide widgets from camera menu.
        self.CameraMenuWidget.show()
        self.FileMenuWidget.hide()
        self.ShowPhotoBtn.hide()
        self.ProcessPhotoBtn.hide()

        # Clear CamTypesBox widget.
        self.CamTypesBox.clear()

        # If available camera doesnt exists do:
        if not self.available_cameras:
            self.CamTypesBox.addItem(str("Nedostupná kamera"))
            self.CamTypesBox.setStyleSheet("background-color: rgba(255, 255, 255, 220);"
                                           "border-color: black;"
                                           "border-radius: 5px;"
                                           "border-width: 3px;"
                                           "color: red;")
            self.CamConnectBtn.hide()
            self.TakePhotoBtn.hide()
        else:
            # Set box of camera types.
            for i in range(len(self.available_cameras)):
                self.CamTypesBox.addItem(self.available_cameras[i].description())

    def connect_camera(self):
        """
            Connect chosen camera to camera viewfinder, created in `create_camera_widgets()`.
            Photo needs to be captured by assigned button and later confirmed for next processing.
        """

        # Show or hide widgets from CameraLayout.
        self.FacePictureLabel.hide()
        self.CameraViewfinder.show()
        self.CameraInfoLabel.hide()
        self.CameraErrorLabel.hide()
        self.ContinueRegBtn.hide()
        self.CameraConfirmLabel.hide()

        # Get camera type from CamTypeBox
        cam_type = self.CamTypesBox.currentText()
        for i in range(len(self.available_cameras)):
            if self.available_cameras[i].description() == cam_type:
                cam_type = i

        # Create QCamera object and connect it to camera device
        self.camera = QtMultimedia.QCamera(self.available_cameras[int(cam_type)])
        self.camera.setViewfinder(self.CameraViewfinder)
        self.camera.setCaptureMode(QtMultimedia.QCamera.CaptureStillImage)
        self.camera.start()

        # Create QCameraImageCapture object to capture photo of user
        self.CameraCapture = QtMultimedia.QCameraImageCapture(self.camera)
        self.FLAG_connected_camera = True

    def capture_photo(self):
        """
            Capture a photo of the user's face with connected camera.
            Photo needs to be confirmed by assigned button.
            The photo is stored in the temporary folder `tmp`.
            The path to a temporary folder can be changed in ``config.py``.
        """

        self.CameraCapture.capture(config.TMP_PHOTO)
        self.ShowPhotoBtn.show()

    def show_photo(self):
        """
            Displays the captured photo in `CameraLayout` for further confirmation.
            Confirmation is executed by assigned button.
        """

        # Show or hide widgets from CameraLayout.
        self.FacePictureLabel.show()
        self.CameraViewfinder.hide()
        self.CameraInfoLabel.hide()
        self.ProcessPhotoBtn.show()
        self.CameraErrorLabel.hide()
        self.ContinueRegBtn.hide()
        self.CameraConfirmLabel.hide()

        # Set pixmap of label.
        face_pixmap = QPixmap(config.TMP_PHOTO)
        self.FacePictureLabel.setPixmap(QPixmap(face_pixmap.scaledToWidth(self.CameraLayoutWidget.width() - 450)))
        self.FacePictureLabel.setAlignment(Qt.AlignCenter)
        # Stop camera recording.
        self.camera.stop()

        # Set flag to 1, camera photo
        self.FLAG_file_type = 1

    def show_file_menu(self):
        """
            Displays the file menu for searching the user's photo file.
        """

        # Reset file type
        self.FLAG_file_type = 0

        # Show or hide widgets from CameraLayout
        self.FacePictureLabel.hide()
        self.CameraViewfinder.hide()
        self.CameraInfoLabel.show()
        self.CameraErrorLabel.hide()
        self.ContinueRegBtn.hide()
        self.CameraConfirmLabel.hide()

        # Show or hide widgets from Menu
        self.FileMenuWidget.show()
        self.CameraMenuWidget.hide()
        self.ChooseFileBtn.hide()
        self.ProcessPhotoBtn.hide()

        # Turn off camera if was started.
        if self.FLAG_connected_camera:
            self.camera.stop()
            self.FLAG_connected_camera = False

    def find_file(self):
        """
            Opens the file dialog to select the desired user face file.
            This file needs to be displayed by assigned button.
            Supported file types are ``.jpg``, ``.gif``, ``.jpeg``.
        """

        self.file_path = QFileDialog.getOpenFileName(self, "Fotka tváre", '', "Image files (*.jpg *.gif *.jpeg)")
        self.FileLineEdit.setText(self.file_path[0])

        if self.FileLineEdit.text() != "":
            self.ChooseFileBtn.show()

    def choose_file(self):
        """
            Displays the selected user face file on `CameraLayout`.
            Image needs to be confirmed by assigned button.
        """

        # Show or hide widgets from CameraLayout
        self.FacePictureLabel.show()
        self.CameraInfoLabel.hide()
        self.ProcessPhotoBtn.show()
        self.CameraErrorLabel.hide()
        self.ContinueRegBtn.hide()
        self.CameraConfirmLabel.hide()

        pixmap = QPixmap(self.file_path[0])
        self.FacePictureLabel.setPixmap(QPixmap(pixmap.scaledToWidth(self.CameraLayoutWidget.width() - 450)))

        # Set flag to 2, file
        self.FLAG_file_type = 2

    def process_photo(self):
        """
            Creates a stimulus from a user's face photo.
            The ``SelfFace`` class is used.
        """

        face_stimuli = None

        # If its camera photo.
        if self.FLAG_file_type == 1:
            face_stimuli = SelfFace(config.TMP_PHOTO)

        # If its chosen file.
        elif self.FLAG_file_type == 2:
            face_stimuli = SelfFace(self.file_path[0])

        if face_stimuli is not None and face_stimuli.get_status():
            im_bytes = base64.b64decode(face_stimuli.get_face_b64())
            im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
            img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

            # READ B64 image as QImage and set it as pixmap on label
            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap(q_img)
            self.FacePictureLabel.setPixmap(QPixmap(pixmap))

            # set user stimulus
            self.reg_user.set_user_stimulus(face_stimuli.get_face_b64())

            self.ContinueRegBtn.show()
            self.ProcessPhotoBtn.hide()
            self.CameraConfirmLabel.show()
        else:
            self.CameraErrorLabel.show()
            self.FacePictureLabel.hide()

    def continue_registration(self):
        """
            It starts the next stage of registration by opening the reg_stimulation_window.
        """

        self.stimuli_window = RegStimuliPresentation(self.reg_user)
        self.stimuli_window.showMaximized()
        self.hide()
