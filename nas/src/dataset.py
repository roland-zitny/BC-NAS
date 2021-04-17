import os
import pickle
from nas.src import config
import nas.main as main_file
import time


class Dataset:
    def __init__(self, reg_data, reg_data_types, login_data, login_data_types):
        self.reg_data = reg_data
        self.reg_data_types = reg_data_types
        self.login_data = login_data
        self.login_data_types = login_data_types

    def save_dataset(self):
        """
            Saves the user object using ``pickle`` library.
            The path where the object is saved can be changed in ``config.py``.
        """
        ts = time.time()
        path = os.path.join(os.path.join(os.path.dirname(main_file.__file__), "datasets", str(ts) + ".p"))
        pickle.dump(self, open(path, "wb"))

    def get_dataset(self):
        return self.reg_data, self.reg_data_types, self.login_data, self.login_data_types
