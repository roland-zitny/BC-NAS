import os
from brainflow.board_shim import BoardIds
import nas.main as main_file

"""
    Configuration file for global variables.
"""

DB_DIR = os.path.join(os.path.dirname(main_file.__file__), "db")  # DB directory path.

TMP_PHOTO = os.path.join(os.path.dirname(main_file.__file__), "db", "tmp", "tmp_photo.jpg")  # Temporary photo path.

# Temp processed photo to save in self face.
TMP_PROC_PHOTO = os.path.join(os.path.dirname(main_file.__file__), "db", "tmp", 'processed_photo.jpg')

NON_FACE_DIR = os.path.join(os.path.dirname(main_file.__file__), "resources", "photos")  # Non Self face stimuli dir.

STARTING_TIME = 5  # Time before recording.

# End windows reaction figures.
TMP_END_FIGURE = os.path.join(os.path.dirname(main_file.__file__), "db", "tmp", 'end_reg_figure.jpg')

EEG_DATASET_FILE = os.path.join(os.path.dirname(main_file.__file__), "db")  # Dir path for creating datasets.

TMP_FOLDER = os.path.join(os.path.dirname(main_file.__file__), "db", "tmp")  # Temp dir path.

# 50 default, 10 self-face, roud(0.2* num) == number of self face stimuli
STIMULI_NUM = 50

CLASSIFICATION = "LDA"  # Classification method. CNN or LDA or BOTH on testing ROC  AUC

# Type of board.
BOARD_TYPE = BoardIds.CYTON_DAISY_BOARD.value  # BoardIds.CYTON_DAISY_BOARD.value / BoardIds.SYNTHETIC_BOARD.value

BOARD_SERIAL_PORT = 'COM7'

# Board Channels
# SYNTH C3,C4,F3,F4 -> 1,3,10,13
# Cyton+DAisy C3,C4,F3,F4 -> 2,3,10,11
