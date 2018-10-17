"""Load csv file with test procedure.

This Module loads a csv file with columns step, time, current in order to
implement an arbitrary load profiles to a DUT.

"""

import csv
import readline
import tab_completer
import time


class event_handler(object):
    """Manages event calls and their callback functions."""

    def __init__(self):
        """Initialize Event Handler."""
        self.function = {}

    def add_function(self, event_name, function):
        """Add event to event list."""
        self.function.update({event_name: function})


class profile_loader(object):
    """Load and run through test profile defined in a .csv."""

    def __init__(self):
        """Initialize loader class."""
        self.events = event_handler()
        self.t = tab_completer.tabCompleter()
        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.t.pathCompleter)

    def load_file(self):
        """Load test profile .csv using an autocompleter."""
        file_path = raw_input("Choose Test Profile [.csv] > ")
        print(" File Chosen : {}".format(file_path))
        self.file = open(file_path)
        self.profile = csv.DictReader(self.file)
        self.read_row()

    def set_start_time(self):
        """Set initial time reference."""
        self.start_time = time.time()

    def run_continuous(self):
        """Run profile continuously."""
        try:
            while(1):
                self.time = time.time() - self.start_time
                if(self.time > self.test_time):
                    self.events.function['set_curr'](current=self.current)
                    volt, curr = self.events.function['read_load']()
                    self.print_profile_row(volt, curr)
                    self.read_row()
        except StopIteration:
            print('Profile end')
            print('Reseting Profile')
            self.reset_profile()
            self.set_start_time()
            self.run_continuous()
        except KeyError:
            print('Wrong csv row name: Try step,time,current')

    def read_row(self):
        """Read csv row and convert to float."""
        row = next(self.profile)

        try:
            self.step = int(row['step'])
            self.test_time = float(row['time'])
            self.current = float(row['current'])
        except KeyError:
            print('Wrong csv row name: Try step,time,current')

    def print_profile_row(self, vload, iload):
        """Print profile row in the terminal."""
        print('{:2.2f}s| step = {} | ts = {:2.2f}s | Isp = {:2.2f}A | Vload = {:2.2f}V | Iload = {:2.2f}A'.format(
            self.time,
            self.step,
            self.test_time,
            self.current,
            vload,
            iload))

    def reset_profile(self):
        """Reset profile csv to start at row 0."""
        self.file.seek(0)
        self.profile = csv.DictReader(self.file)
        self.read_row()






if __name__ == '__main__':

    # User Functions
    def set_current(current=None):
        print('Setting current to {}'.format(current))

    def read_load():
        return 12.2, 3.0

    loader = profile_loader()
    loader.events.add_function('set_curr', set_current)
    loader.events.add_function('read_load', read_load)
    loader.load_file()
    loader.set_start_time()
    loader.run_continuous()
