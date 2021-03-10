import pickle
from datetime import datetime
import time
import numpy as np
from pyOpenBCI import OpenBCICyton


class EEGRecorder():
    def __init__(self):
        self.board = None
        self.timestamps = np.array([])
        self.data = np.array([])

    def print_raw(self, sample):
        timestamp = datetime.now()
        self.timestamps = np.append(self.timestamps, timestamp)
        self.data = np.append(np.asarray(sample.channels_data))

    def start_record(self):
        self.board = OpenBCICyton(port="COM7", daisy=True)
        self.board.start_stream(self.print_raw)

    def stop_record(self):
        try:
            self.board.stop_stream()
        except:
            print("EXCEPT V EEG RECORDER STOp RECORD")

    def get_timestamps(self):
        return self.timestamps

    def get_data(self):
        return self.data
