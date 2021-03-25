import brainflow
import numpy as np
from matplotlib import pyplot as plt
from brainflow import BoardShim, BoardIds, DataFilter, AggOperations, FilterTypes
from nas.src import config


class DataProcessing():
    """
        Class used to process and filter EEG data recorded by Brainflow library.

        Attributes
        ----------
        data : numpy array
            whole EEG data, 15 channels

        timestamps : numpy array
            timestamps of EEG data

        stimuli_timestamps :
            timestamps of stimuli

        stim_num :
            number of stimuli

        Methods
        -------
        filter_data :
            Data filtering.

        create_epochs :
            Gets stimuli time windows.
    """

    def __init__(self, data, timestamps, stimuli_timestamps, stimuli_num):
        self.data = data
        self.timestamps = timestamps
        self.stimuli_timestamps = stimuli_timestamps
        self.num_of_stimuli = stimuli_num

    def filter_data(self):
        """
            Method to filter and clean data.
        """

        # BANDSTOP & Wavelet denoising TODO
        for i in range(16):
            DataFilter.perform_bandstop(self.data[i], 256, 55.0, 10.0, 3,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_wavelet_denoising(self.data[i], 'coif3', 3)

        print("vyfiltrovane")

    def create_epochs(self):
        """
            Method to get stimuli time windows.
        """

        # TODO pridat dalsie features ako integral max min atd co bude vhodne to sa este nevie
        stimuli_epochs = []
        num_of_x = round(BoardShim.get_sampling_rate(config.BOARD_TYPE) * 0.6)

        for i in range(self.num_of_stimuli):
            stimuli_time_ms = self.stimuli_timestamps[i] * 1000

            F3 = np.array([])
            F4 = np.array([])
            C3 = np.array([])
            C4 = np.array([])

            for y in range(len(self.timestamps)):
                eeg_timestamp_ms = self.timestamps[y] * 1000
                if eeg_timestamp_ms >= stimuli_time_ms - 50 and len(F3) < num_of_x:
                    F3 = np.append(F3, self.data[10, y])
                    F4 = np.append(F4, self.data[11, y])
                    C3 = np.append(C3, self.data[2, y])
                    C4 = np.append(C4, self.data[3, y])

            epoch = np.array([F3, F4, C3, C4])
            stimuli_epochs.append(epoch)

        return stimuli_epochs
