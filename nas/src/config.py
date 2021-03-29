import os
from brainflow.board_shim import BoardIds
from nas import main as main_file

"""
    Configuration file for global variables.
"""

DB_DIR = os.path.join(os.path.dirname(main_file.__file__), "db")  # DB directory path.
TMP_PHOTO = os.path.join(os.path.dirname(main_file.__file__), "db", "tmp", "tmp_photo.jpg")  # Temporary photo path.
NON_FACE_DIR = os.path.join(os.path.dirname(main_file.__file__), "resources", "photos")     # Non Self face stimuli
STARTING_TIME = 5
# 50 default, 10 self-face, possible 30;40 ... every fifth is stimuli
STIMULI_NUM = 5
BOARD_TYPE = BoardIds.SYNTHETIC_BOARD.value     #BoardIds.CYTON_DAISY_BOARD.value / BoardIds.SYNTHETIC_BOARD.value
BOARD_SERIAL_PORT = 'COM7'
# SYNTH C3,C4,F3,F4 -> 1,3,10,13
# Cyton+DAisy C3,C4,F3,F4 -> 2,3,10,11
