import time

from brainflow import DataFilter
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from nas.src import config
import pandas as pd
import numpy as np


class EEGRecorder:
    """
        Class used to record EEG data of user.

        Attributes
        ----------
        None

        Methods
        -------
        start_record():
            Recording session.

        stop_record():
            Stops session.

        get_rec_data():
            Data getter.

        get_rec_timestamps():
            Timestamps getter.

    """

    def __init__(self):
        self.board = None
        self.data = None
        self.timestamps = None

    def start_record(self):
        """
            Start recording session.
        """

        params = BrainFlowInputParams()
        params.ip_port = 0
        params.serial_port = config.BOARD_SERIAL_PORT
        params.mac_address = ''
        params.other_info = ''
        params.serial_number = ''
        params.ip_address = ''
        params.ip_protocol = 0
        params.timeout = 0
        params.file = ''

        # 0 = Cyton, 2 = Cyton + Daisy, -1 synth
        self.board = BoardShim(config.BOARD_TYPE, params)
        self.board.disable_board_logger()
        BoardShim.prepare_session(self.board)
        BoardShim.start_stream(self.board)

    def stop_record(self):
        """
            Stops session.
        """

        self.data = self.board.get_board_data()
        eeg_channels = BoardShim.get_eeg_channels(config.BOARD_TYPE)
        self.timestamps = BoardShim.get_timestamp_channel(config.BOARD_TYPE)
        self.board.stop_stream()
        BoardShim.release_session(self.board)

        # SAVE DATA TODO
        #print(len(self.data[0]))
        #file_name = str(round(time.time() * 1000))
        #DataFilter.write_file(self.data, file_name + '.csv', 'w')
        self.timestamps = self.data[self.timestamps]
        self.data = self.data[eeg_channels]

    def get_rec_data(self):
        """
            asdsa
        """

        return self.data

    def get_rec_timestamps(self):
        """
            asdsa
        """

        return self.timestamps


if __name__ == '__main__':
    recorder = EEGRecorder()
    recorder.start_record()
    time.sleep(10)
    recorder.stop_record()
