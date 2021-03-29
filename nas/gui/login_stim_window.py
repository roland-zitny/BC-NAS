import time
import numpy as np
from threading import Thread

import scipy
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget
from nas.src import config
from nas.src.eeg_recorder import EEGRecorder
from nas.src.data_processing import DataProcessing
from nas.src.stimuli_creator import StimuliCreator
from datetime import datetime
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from nas.src.classifier import Classifier

qt_stimuli_presentation_file = "gui/designs/login_stimuli_window.ui"  # .ui file.
Ui_RegWindow, QtBaseClass = uic.loadUiType(qt_stimuli_presentation_file)


class LoginStimuliPresentation(QtWidgets.QMainWindow, Ui_RegWindow):
    """
        Class used to obtain EEG data from user for his login.

        Attributes
        ----------
        reg_user : object
            object of registered user

        Methods
        -------
        set_up_window()
            Set up all necessary parameters of window.

        start_recording()
            Starts EEG recording with class eeg_recorder.

        update_start_time()
            Starting timer.

        stimulation()
            Stimulation timer.

        update_stimuli()
            Update types of stimulus.

    """

    def __init__(self, reg_user):
        QtWidgets.QMainWindow.__init__(self)
        Ui_RegWindow.__init__(self)
        self.setupUi(self)
        self.reg_user = reg_user  # Object with user, his name, surname and image/stimulus.
        self.stimuli_types_array = ""  # Array of stimulus types.
        self.stimuli_timestamps = np.array([])  # Array of stimuli timestamps.
        self.eeg_recorder = None
        self.recording_thread = None
        self.stimuli_creator = StimuliCreator(self.reg_user.get_user_stimulus())

        # Start timer.
        self.starting_time = config.STARTING_TIME
        self.FLAG_start_timer = True
        self.StartTimer = QTimer(self)
        self.StartTimer.timeout.connect(self.update_start_time)

        # Stimuli timer.
        self.stimuli_time = 0
        self.num_of_stimuli = 0
        self.FLAG_stimuli_timer = True
        self.StimuliTimer = QTimer(self)
        self.StimuliTimer.timeout.connect(self.update_stimuli)

        # Flags for stimuli type.
        self.FLAG_stimulus = False
        self.FLAG_blank = True
        self.FLAG_change = True  # Flag of change, to not call pixmap method multiple times.
        self.time_memory = 0  # Memory of time.

        self.set_up_window()

    def set_up_window(self):
        """
            Set up additional parameters of window.
        """

        # Center window to screen.
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Hide unnecessary widgets.
        self.StimuliLayoutWidget.hide()
        self.StimuliImage.hide()

        # Connect ui buttons to methods.
        self.StartRecording.clicked.connect(self.start_recording)

        # TODO
        # self.test()

    def start_recording(self):
        """
            Starts EEG recording with eeg_recorder.py.
            To record we need to use thread.
        """

        self.StimuliInfoWidget.hide()
        self.StimuliLayoutWidget.show()
        self.StartTimer.start(1000)
        self.eeg_recorder = EEGRecorder()
        self.recording_thread = Thread(target=self.eeg_recorder.start_record)
        self.recording_thread.daemon = True  # Thread exits if app is closed.
        print("start:", end="")
        print(time.time())
        now = datetime.now()
        print(now)
        self.recording_thread.start()

    def update_start_time(self):
        """
            Timer before stimulation and counting.
            Default is 5 sec.
        """

        if self.FLAG_start_timer:
            self.starting_time -= 1
            self.StartTimerLabel.setText(str(self.starting_time))

            if self.starting_time == 0:
                self.FLAG_start_timer = False
                self.StartTimer.stop()
                self.StartTimerLabel.hide()
                self.stimulation()

    def stimulation(self):
        """
            Stimulation timer, used to change stimulus.
        """

        self.StimuliTimer.start(10)  # 0.1 s / 100 ms
        self.StimuliImage.show()

    def update_stimuli(self):
        """
            Change stimuli pixmap.
            Self-face or non-self-face.
        """

        if self.FLAG_stimuli_timer:
            self.stimuli_time += 0.01
            self.stimuli_time = round(self.stimuli_time, 2)

            if self.num_of_stimuli == config.STIMULI_NUM + 1:  # Number of stimuli. TODO +1 lebo aby zaznamenal na
                # TODO posledny stimul dostatok
                self.FLAG_stimuli_timer = False
                self.StimuliTimer.stop()
                self.eeg_recorder.stop_record()  # Stop recording.
                # self.end_registration()
                # TODO TEST
                #print("end:", end="")
                #print(time.time())
                #now = datetime.now()
                #print(now)
                #self.test()
                self.test2()

        if self.FLAG_stimuli_timer:
            if self.FLAG_stimulus:
                if self.FLAG_change:
                    pixmap = self.stimuli_creator.randomized_stimuli()
                    # Save stimuli timestamps.
                    stimuli_timestamp = time.time()
                    self.stimuli_timestamps = np.append(self.stimuli_timestamps, stimuli_timestamp)
                    self.StimuliImage.setPixmap(QPixmap(pixmap))
                    self.FLAG_change = False

                if self.stimuli_time == round(self.time_memory + 0.3, 2):  # TODO add random na 0.3
                    self.time_memory = self.stimuli_time
                    self.num_of_stimuli += 1
                    self.FLAG_stimulus = False
                    self.FLAG_blank = True
                    self.FLAG_change = True

            if self.FLAG_blank:
                if self.FLAG_change:
                    self.StimuliImage.clear()
                    self.FLAG_change = False

                if self.stimuli_time == round(self.time_memory + 1.0, 2):  # TODO add random na 1.0
                    self.time_memory = self.stimuli_time
                    self.FLAG_stimulus = True
                    self.FLAG_blank = False
                    self.FLAG_change = True


    def test2(self):
        data = self.eeg_recorder.get_rec_data()
        timestamps = self.eeg_recorder.get_rec_timestamps()
        data_processing = DataProcessing(data, timestamps, self.stimuli_timestamps, config.STIMULI_NUM)
        data_processing.filter_data()

        # LOGIN DATA
        stimuli_epochs = data_processing.create_epochs()
        # REG DATA
        epochs, types = self.reg_user.get_test_data()
        # LOGIN STIM TYPES
        login_stimuli_types = self.stimuli_creator.get_stimuli_types()

        classifier = Classifier(stimuli_epochs, epochs, types)
        classifier.reduce_dimension_lda()
        result = classifier.classifie("LDA")

        print(result)
        print("ASDASDASDASDSADSA")
        print(login_stimuli_types[:-1])

