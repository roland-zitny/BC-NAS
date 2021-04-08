====================
Installation & usage
====================

This part of documentation represents process of installation and usage.

.. toctree::
   :maxdepth: 2

Installation
====================
To start the system, a python interpreter version `3.8` is required due to the `tensorflow <https://www.tensorflow.org/>`_ library,
which was not supported by a higher version at the time of implementation.
The project contains a ``requirements.txt`` file, which contains a list of all necessary libraries that must be installed.



Usage
====================

* After starting the system, you can choose the option to `register` or `log in`.

Registration
-------------

* When registering, it is necessary to create a stimulus for the user, thanks to a photo of his face.
  This photo can be created using a connected camera or selecting a photo file.

* After the stimulus is created, the recording of the user's EEG signals begins.
  To do this, it is necessary to have a device connected that allows this recording.
  During the implementation, a device from `OpenBCI <https://openbci.com/>`_ was used, namely the
  `Cyton + Daisy` version which contains 16 electrodes.

* After successful registration, an exit window will appear.

Login
------------

* It is no longer necessary to create a user stimulus when logging in, but it is necessary to record EEG signals.

* After the EEG signals are recorded correctly, they will be processed and classified. Such data then determines the
  success of the login.

* The last step is to display a window that notifies the user of the login success.