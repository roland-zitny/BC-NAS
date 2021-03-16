import brainflow
import numpy as np
from matplotlib import pyplot as plt
from brainflow import BoardShim, BoardIds, DataFilter, AggOperations, FilterTypes


class DataProcessing():
    def __init__(self, data, timestamps, stimuli_timestamps, stim_num):
        self.data = data
        self.timestamps = timestamps
        self.stimuli_timestamps = stimuli_timestamps
        self.num_of_stimuli = stim_num

    def filter_data(self):
        # BANDSTOP & Wavelet denoising TODO
        for i in range(16):
            DataFilter.perform_bandstop(self.data[i], 256, 55.0, 10.0, 3,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_wavelet_denoising(self.data[i], 'coif3', 3)

    def create_epochs(self):
        stimuli_epochs = []
        for i in range(self.num_of_stimuli - 1):
            stimuli_time_ms = self.stimuli_timestamps[i] * 1000

            F3 = np.array([])
            F4 = np.array([])
            C3 = np.array([])
            C4 = np.array([])

            for y in range(len(self.timestamps)):
                eeg_timestamp_ms = self.timestamps[y] * 1000
                # 800 ms time window
                # Je moznost ist aj cez sampling rate , cize tu je 256/2 * 0.6  a dostaneme pocet vzoriek na 0.6 sec.
                # Je mozne pracovat s casom. TODO
                # 100 je data ako 256/2 * 0.8
                # Pre daisy+ cyton 125 / 2 * 0.8 -> 50 segmentov
                if eeg_timestamp_ms >= stimuli_time_ms - 50 and eeg_timestamp_ms <= stimuli_time_ms + 750:
                    if len(F3) < 100:
                        F3 = np.append(F3, self.data[10, y])
                        F4 = np.append(F4, self.data[11, y])
                        C3 = np.append(C3, self.data[2, y])
                        C4 = np.append(C4, self.data[3, y])

            epoch = np.array([F3, F4, C3, C4])
            stimuli_epochs.append(epoch)

        return stimuli_epochs
