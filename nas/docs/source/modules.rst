==========
Modules
==========

The `Neural Access System` modules are divided into two sections, namely ``gui`` and ``src``.
The ``gui`` section contains another folder with the designs of individual graphical user windows.
These designs were created using `qt designer <https://doc.qt.io/qt-5/qtdesigner-manual.html>`_.
The project also contains a ``db`` folder for registered users and a ``db`` folder also contains
a ``tmp`` folder for temporarily storing the files needed for the registration itself.
The ``resources`` folder is used to store `non-self-face` stimuli and necessary
images for the graphical user interface.

Most modules contain preset values for some parameters, which you can edit in the ``config.py`` file.
For information about the ``config.py`` file, visit the `configuration` chapter.

.. toctree::
   :maxdepth: 2

Main File
===================
.. automodule:: nas.main
   :members:

Graphic User Interface
======================
The graphical user interface consists of four windows,
namely ``MainWindow``, ``RegistrationWindow`` , ``RegStimulationWindow`` and
``LoginStimulationWindow``.

MainWindow
----------------------
.. automodule:: nas.gui.main_window
   :members:

RegistrationWindow
----------------------
.. automodule:: nas.gui.registration_window
    :members:

RegStimulationPresentation
--------------------------
.. automodule:: nas.gui.reg_stimulation_window
    :members:

LoginStimulationPresentation
----------------------------
.. automodule:: nas.gui.login_stimulation_window
    :members:

EndRegistrationWindow
----------------------------
.. automodule:: nas.gui.end_registration_window
    :members:

EndLoginWindow
----------------------------
.. automodule:: nas.gui.end_login_window
    :members:

Source
===================
Source files consist of ``user``, ``self_face``, ``stimuli_creator``, ``eeg_recorder``
, ``data_processing`` and ``classifier``.

User
----------------------
.. automodule:: nas.src.user
   :members:

SelfFace
-----------------------
.. automodule:: nas.src.self_face
    :members:

StimuliCreator
-----------------------
.. automodule:: nas.src.stimuli_creator
    :members:

EEGRecorder
-----------------------
.. automodule:: nas.src.eeg_recorder
    :members:

DataProcessing
-----------------------
.. automodule:: nas.src.data_processing
    :members:

Classifier
-----------------------
.. automodule:: nas.src.classifier
    :members:



