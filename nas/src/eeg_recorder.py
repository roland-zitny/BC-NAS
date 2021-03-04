from pyOpenBCI import OpenBCICyton

class EEGRecorder():
    def __init__(self):
        print("EEG recorder created")
        self.f = open("eeg.txt", "a")

    def print_raw(self, sample):
        #mal byt timestamp
        print(sample.start_time)
        print(sample.channels_data)

        self.f.write(sample.start_time)
        self.f.write("\n")
        self.f.write(sample.channels_data)
        self.f.wite("\n")

    def start_record(self):
        # board = OpenBCICyton(daisy=True) --> port vie sam vyhladat
        # moznost COM6 este
        try:
            #self.board = OpenBCICyton(port="COM6", daisy=True)
            #Start time timestamp
            #print(self.board.start_time)
            # Start stream and print it raw
            print("START RECORD")
            #self.board.start_stream(self.print_raw)
        except:
            print("CHYBA NAHRVANIA")

    def stop_record(self):
        self.f.close()

        try:
            print("STOP RECORD")
            self.board.stop_stream()
        except:
            print("CHYBA UKONCENIA")