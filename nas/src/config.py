import os
from brainflow.board_shim import BoardIds
from nas import main as main_file

"""
    Configuration file for global variables.
"""

DB_DIR = os.path.join(os.path.dirname(main_file.__file__), "db")  # DB directory path.
TMP_PHOTO = os.path.join(os.path.dirname(main_file.__file__), "db", "tmp", "tmp_photo.jpg")  # Temporary photo path.
STARTING_TIME = 5
STIMULI_NUM = 30
BOARD_TYPE = BoardIds.SYNTHETIC_BOARD.value
