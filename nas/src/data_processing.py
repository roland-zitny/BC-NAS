import numpy as np
from brainflow import BoardShim, DataFilter, FilterTypes, AggOperations
from nas.src import config


class DataProcessing:
    """
        A class that processes and filters EEG data.

        :param data: EEG data.
        :type data: numpy.array

        :param timestamps: EEG data timestamps.
        :type timestamps: numpy.array

        :param stimuli_timestamps: Timestamps of stimulation.
        :type stimuli_timestamps: numpy.array

        :param stimuli_num: Number of stimules.
        :type stimuli_num: int
    """

    def __init__(self, data, timestamps, stimuli_timestamps, stimuli_num):
        self.data = data
        self.timestamps = timestamps
        self.stimuli_timestamps = stimuli_timestamps
        self.num_of_stimuli = stimuli_num

    def filter_data(self):
        """
            Filters data from unwanted artifacts and filters noise.
        """

        #db8/ coif3
        for i in range(16):
            DataFilter.perform_bandstop(self.data[i], 256, 55.0, 10.0, 3,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_wavelet_denoising(self.data[i], 'db8', 3)
            #DataFilter.perform_rolling_filter(self.data[i],  3, AggOperations.MEAN.value)

    def create_time_windows(self):
        """
            Method to get stimuli time windows.

            :return: List of time windows.
            :rtype: list
        """

        stimuli_epochs = []
        num_of_x = round(BoardShim.get_sampling_rate(config.BOARD_TYPE) * 0.8)

        for i in range(self.num_of_stimuli):
            stimuli_time_ms = self.stimuli_timestamps[i] * 1000

            F3 = np.array([])
            F4 = np.array([])
            C3 = np.array([])
            C4 = np.array([])

            for y in range(len(self.timestamps)):
                eeg_timestamp_ms = self.timestamps[y] * 1000
                if eeg_timestamp_ms >= stimuli_time_ms and len(F3) < num_of_x:
                    F3 = np.append(F3, self.data[10, y])
                    F4 = np.append(F4, self.data[11, y])
                    C3 = np.append(C3, self.data[2, y])
                    C4 = np.append(C4, self.data[3, y])

            epoch = np.array([F3, F4, C3, C4])
            stimuli_epochs.append(epoch)

        return stimuli_epochs
