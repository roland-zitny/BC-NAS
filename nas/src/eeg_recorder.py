from pyOpenBCI import OpenBCICyton

class EEGRecorder():
    def __init__(self):
        print("EEG recorder created")

    def print_raw(sample):
        #mal byt timestamp
        #print(sample.start_time)

        print(sample.channels_data)


    def start_record(self):
        # board = OpenBCICyton(daisy=True) --> port vie sam vyhladat
        # moznost COM6 este
        self.board = OpenBCICyton(port="COM5", daisy=True)

        #Start time timestamp
        #print(self.board.start_time)


        # Start stream and print it raw
        print("START RECORD")
        #self.board.start_stream(self.print_raw)

    def stop_record(self):
        print("STOP RECORD")
        #self.board.stop_stream()
        pass