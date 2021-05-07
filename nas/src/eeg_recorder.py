from brainflow.board_shim import BoardShim, BrainFlowInputParams
from nas.src import config


class EEGRecorder:
    """
        Class for recording EEG signals.
    """

    def __init__(self):
        self.board = None
        self.data = None
        self.timestamps = None

    def start_record(self):
        """
            Starts recording session.
        """

        params = BrainFlowInputParams()
        params.ip_port = 0
        params.serial_port = config.BOARD_SERIAL_PORT
        params.mac_address = ''
        params.other_info = ''
        params.serial_number = ''
        params.ip_address = ''
        params.ip_protocol = 0
        params.timeout = 0
        params.file = ''

        # 0 = Cyton, 2 = Cyton + Daisy, -1 synth
        self.board = BoardShim(config.BOARD_TYPE, params)
        self.board.disable_board_logger()
        BoardShim.prepare_session(self.board)
        BoardShim.start_stream(self.board)

    def stop_record(self):
        """
            Stops recording session.
        """

        self.data = self.board.get_board_data()
        eeg_channels = BoardShim.get_eeg_channels(config.BOARD_TYPE)
        self.timestamps = BoardShim.get_timestamp_channel(config.BOARD_TYPE)
        self.board.stop_stream()
        BoardShim.release_session(self.board)

        # TODO SAVING WHOLE DATA
        # file_name = str(round(time.time() * 1000))
        # DataFilter.write_file(self.data, file_name + '.csv', 'w')

        self.timestamps = self.data[self.timestamps]
        self.data = self.data[eeg_channels]

    def get_rec_data(self):
        """
            EEG data getter.

            :return: Array of EEG data.
            :rtype: numpy.array
        """

        return self.data

    def get_rec_timestamps(self):
        """
            Timestamps getter.

            :return: Data timestamps.
            :rtype: numpy.array
        """

        return self.timestamps
