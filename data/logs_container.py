import threading


class LogsContainer:
    """ Thread safe class encapsulating list. Should handle Log instances. """

    def __init__(self):
        self._logs = []
        self._cv = threading.Condition()
        self._iter_index = 0

    def append(self, log):
        with self._cv:
            self._logs.append(log)
            self._cv.notify()

    def reset(self):
        with self._cv:
            self._logs = []     #todo ok?
            self._cv.notify()

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        if self._iter_index == len(self._logs):
            raise StopIteration
        log = self._logs[self._iter_index]
        self._iter_index += 1
        return log

    def __getitem__(self, item):
        return self._logs[item]

    def __len__(self):
        return len(self._logs)