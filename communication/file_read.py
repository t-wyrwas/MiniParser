__author__ = 'twyrwas'


class DumpFileReader:

    def __init__(self, container, filename):
        self._container = container
        self._filename = filename
        self._run = False
        self._file_to_read = None

    def run(self):
        self._run = True
        self._file_to_read = open(self._filename, 'r')
        log = self._file_to_read.readline()
        while log:
            self._container.append(log)
            log = self._file_to_read.readline()
            if self._run == False:
                self._file_to_read.flush()
                self._file_to_read.close()
                break

    def stop(self):
        if self._run is True:
            self._run = False
