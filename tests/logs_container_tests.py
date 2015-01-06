from data import logs_container

__author__ = 'twyrwas'

import unittest
import data.log


class LogsContainerTests(unittest.TestCase):

    def setUp(self):
        self._container = logs_container.LogsContainer()
        lines = self._read_logs()
        self._logs = list()
        for line in lines:
            log = data.log.Log(line)
            self._logs.append(log)
            self._container.append(log)

    def test_iteration(self):
        i = 0
        for log in self._container:
            msg = log.get_part('Message')
            if len(msg) != 0:
                i += 1
        self.assertEqual(i, len(self._logs))

    def test_len_and_reset(self):
        self.assertEqual(len(self._logs), len(self._container))
        self._container.reset()
        self.assertEqual(0, len(self._container))

    def test_getitem(self):
        length = len(self._container)
        middle = length/2
        log_first = self._container[0]
        log_middle = self._container[middle]
        log_last = self._container[length-1]
        self.assertEqual(log_first, self._logs[0])
        self.assertEqual(log_middle, self._logs[middle])
        self.assertEqual(log_last, self._logs[length-1])

    def test_getitem_range(self):
        length = len(self._container)
        middle = length/2
        second_half = self._container[middle:length]
        expected_second_half = self._logs[middle:length]
        i = 0
        for log in second_half:
            self.assertEqual(log, expected_second_half[i])
            i += 1

    def _read_logs(self):
        file = open('dummy_logs', 'r')
        line = file.readline()
        logs = list()
        while line:
            logs.append(line)
            line = file.readline()
        return logs

suite = unittest.TestLoader().loadTestsFromTestCase(LogsContainerTests)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)