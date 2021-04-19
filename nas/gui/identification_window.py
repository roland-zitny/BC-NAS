import time
import numpy as np
from threading import Thread
import os
from datetime import datetime
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget
import nas.src.config as config
from nas.src.eeg_recorder import EEGRecorder
from nas.src.data_processing import DataProcessing
from nas.src.stimuli_creator import StimuliCreator
from nas.src.classifier import Classifier
from nas.gui.end_login_window import EndLoginWindow

directory_path = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(directory_path, "designs" + os.sep + "identification_stimuli_window.ui")
Ui_RegWindow, QtBaseClass = uic.loadUiType(ui_path)


class IdentStimulationPresentation(QtWidgets.QMainWindow, Ui_RegWindow):
    """
        IDENTIFICATION
    """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_RegWindow.__init__(self)
        self.setupUi(self)
        self.stimuli_types_array = ""  # Array of stimulus types.
        self.stimuli_timestamps = np.array([])  # Array of stimuli timestamps.
        self.eeg_recorder = None
        self.recording_thread = None
        self.end_login_window = None
        self.stimuli_creator = StimuliCreator()
        self.stimuli_creator.set_up_identification_data()
        self.identification_counter = self.stimuli_creator.get_identification_users_num()

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
            Makes other window settings, such as connecting buttons, etc.
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

    def start_recording(self):
        """
            Starts recording EEG signals. It is necessary to use a thread for proper functionality.
        """

        self.StimuliInfoWidget.hide()
        self.StimuliLayoutWidget.show()
        self.StartTimer.start(1000)
        self.eeg_recorder = EEGRecorder()
        self.recording_thread = Thread(target=self.eeg_recorder.start_record)
        self.recording_thread.daemon = True  # Thread exits if app is closed.
        self.recording_thread.start()

    def update_start_time(self):
        """
            Stimulation start timer.
            The default is set to 5 seconds, but this time can be changed in the ``conf.py`` file.
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
            Timer of the stimulation itself
        """

        self.StimuliTimer.start(10)  # 0.1 s / 100 ms
        self.StimuliImage.show()

    def update_stimuli(self):
        """
            Updates the stimulus type.
            StimuliCreator is used.
            Each stimulus is timed to 0.3 seconds followed by 1 second of the blank screen.
        """

        if self.FLAG_stimuli_timer:
            self.stimuli_time += 0.01
            self.stimuli_time = round(self.stimuli_time, 2)

            if self.num_of_stimuli == self.identification_counter + 1:  # Number of stimuli +1 because of time synchronization.
                self.FLAG_stimuli_timer = False
                self.StimuliTimer.stop()
                self.eeg_recorder.stop_record()  # Stop recording.
                self.get_identification_data()

        if self.FLAG_stimuli_timer:
            if self.FLAG_stimulus:
                if self.FLAG_change:
                    pixmap = self.stimuli_creator.identification_stimuli()
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

    def get_identification_data(self):
        """
            TODO
        """

        possible_ids = self.stimuli_creator.get_all_ids()

        # EEG Data
        data = self.eeg_recorder.get_rec_data()
        timestamps = self.eeg_recorder.get_rec_timestamps()
        data_processing = DataProcessing(data, timestamps, self.stimuli_timestamps, config.STIMULI_NUM)
        data_processing.filter_data()

        # Stimuli windows, stimuli types
        stimuli_windows = data_processing.create_time_windows()
        stimuli_types = self.stimuli_creator.get_stimuli_types()

        # Reg data of all users -- concatenated
        reg_data = []

        for i in range(len(possible_ids)):
            path = os.path.join(config.DB_DIR + os.sep + possible_ids[i])  # DB directory path.
            print(path)