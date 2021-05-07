import os
import pickle
from nas.src import config
import nas.main as main_file
import time


class DatasetRaw:
    def __init__(self, raw_data, data_timestamps, stimuli_timestamps, number_of_stim, stimuli_types):
        self.raw_data = raw_data
        self.data_timestamps = data_timestamps
        self.stimuli_timestamps = stimuli_timestamps
        self.number_of_stim = number_of_stim
        self.stimuli_types = stimuli_types

    def save_dataset(self):
        """
            Saves the user object using ``pickle`` library.
            The path where the object is saved can be changed in ``config.py``.
        """
        ts = time.time()
        path = os.path.join(os.path.join(os.path.dirname(main_file.__file__), "datasets", str(ts) + ".p"))
        pickle.dump(self, open(path, "wb"))

    def get_dataset(self):
        return self.raw_data, self.data_timestamps, self.stimuli_timestamps, self.number_of_stim, self.stimuli_types
