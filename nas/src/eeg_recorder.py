import argparse
import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes

class EEGRecorder_brainflow():
    def __init__(self):
        self.board = None
        self.data = None
        self.timestamps = None

    def start_record(self):
        print("start")
        params = BrainFlowInputParams()
        params.ip_port = 0
        params.serial_port = 'COM7'
        params.mac_address = ''
        params.other_info = ''
        params.serial_number = ''
        params.ip_address = ''
        params.ip_protocol = 0
        params.timeout = 0
        params.file = ''


        # 0 = Cyton, 2 = Cyton + Daisy, -1 synth
        #self.board = BoardShim(-1, params)
        #self.board.start_stream(45000, '')
        #print("NEPODARILO SA PRIPOJIT BOARD")
        self.board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
        self.board.disable_board_logger()
        BoardShim.prepare_session(self.board)
        BoardShim.start_stream(self.board)

    def stop_record(self):
        self.data = self.board.get_board_data()
        eeg_channels = BoardShim.get_eeg_channels(-1)
        self.timestamps = BoardShim.get_timestamp_channel(-1)   # 2 later
        self.board.stop_stream()
        BoardShim.release_session(self.board)

        self.timestamps = self.data[self.timestamps]
        self.data = self.data[eeg_channels]

    def get_rec_data(self):
        return self.data

    def get_rec_timestamps(self):
        return self.timestamps


if __name__ == '__main__':
    recorder = EEGRecorder_brainflow()
    recorder.start_record()
    time.sleep(10)
    recorder.stop_record()
