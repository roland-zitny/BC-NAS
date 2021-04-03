import os
import pickle
from nas.src import config


class User:
    """
        Class for creating a user object and storing it.

        :param name: User name.
        :type name: string
        :param surname: User surname.
        :type surname: string
        :param login_id: User login ID.
        :type login_id: string
    """

    def __init__(self, name, surname, login_id):
        self.login_id = login_id
        self.name = name
        self.surname = surname
        self.stimulus_b64 = None
        self.user_stimuli_windows = None
        self.window_types = None

    def set_user_stimulus(self, stimulus):
        """
            User's stimulus setter.

            :param stimulus: Picture of a user's face.
            :type stimulus: base64 string
        """

        self.stimulus_b64 = stimulus

    def get_user_stimulus(self):
        """
            User's stimulus getter.

            :return: Picture of a user's face.
            :rtype: base64 string
        """
        return self.stimulus_b64

    def set_reg_data(self, user_stimuli_windows, window_types):
        """
            Registration data setter.
            Length of `user_stimuli_windows` and `window_types` must be the same.

            :param user_stimuli_windows: User responses to stimuli divided into time windows.
            :type user_stimuli_windows: list TODO
            :param window_types: Types of individual time windows. 1 for self-face and 0 for non-self-face.
            :type window_types: list TODO
        """

        self.user_stimuli_windows = user_stimuli_windows
        self.window_types = window_types

    def get_reg_data(self):
        """
            Registration data getter.

            :return: user_stimuli_windows, window_types
            :rtype: list, list
        """

        return self.user_stimuli_windows, self.window_types

    def save_user(self):
        """
            Saves the user object using ``pickle`` library.
            The path where the object is saved can be changed in ``config.py``.
        """

        path = os.path.join(config.DB_DIR, self.login_id + ".p")
        pickle.dump(self, open(path, "wb"))

    def get_name(self):
        """
            User name getter.

            :return: User name.
            :rtype: string
        """

        return self.name

    def get_surname(self):
        """
            User surname getter.

            :return: User surname.
            :rtype: string
        """

        return self.surname

    def get_id(self):
        """
            User id getter.

            :return: User id.
            :rtype: string
        """

        return self.login_id