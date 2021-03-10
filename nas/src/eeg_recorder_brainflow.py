import argparse
import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
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

        try:
            # 0 = Cyton, 2 = Cyton + Daisy
            self.board = BoardShim(2, params)
            self.board.start_stream(45000, '')
        except:
            print("NEPODARILO SA PRIPOJIT BOARD")

    def stop_record(self):
        try:
            self.data = self.board.get_board_data()
            self.timestamps = self.get_timestamp_channel(2)
            self.board.stop_stream()
            self.release_session()
        except:
            print("NEPRIPOJILA SA DOSKA")

    def get_rec_data(self):
        return self.data

    def get_rec_timestamps(self):
        return self.timestamps


if __name__ == '__main__':
    recorder = EEGRecorder_brainflow()
    recorder.start_record()
    time.sleep(10)
    recorder.stop_record()
