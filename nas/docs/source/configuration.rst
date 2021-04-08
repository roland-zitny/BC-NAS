====================
Configuration
====================

The project contains a ``config.py`` file in the ``src`` folder. This file is used to set the values of all parameters
that affect the operation of the application.


The file contains these parameters:

``DB_DIR``              -  Path to saved registered users.


``TMP_PHOTO``           -  Path to the user's temporarily captured face.


``TMP_PROC_PHOTO``      -  Path to the user's temporarily processed photo.


``NON_FACE_DIR``        -  The path to `non-self-face` stimuli.


``STARTING_TIME``       -  Starting time of stimulation.


``TMP_END_FIGURE``      -  Path for saving the resulting graph of reactions.


``EEG_DATASET_FILE``    -  Path to the place where the dataset is created for further analysis.


``STIMULI_NUM``         -  Number of stimuli displayed.


``CLASSIFICATION``      - Classification method. [CNN, LDA]


``BOARD_TYPE``          -  Type of board connected for EEG recording using the `brainflow <https://brainflow.readthedocs.io/en/stable/SupportedBoards.html>`_ library.


``BOARD_SERIAL_PORT``   -  Serial port of recording device if needed.

.. toctree::
   :maxdepth: 2