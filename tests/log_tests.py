__author__ = 'twyrwas'
import unittest
import logger_configuration
import data.log


class LogTests(unittest.TestCase):

    def setUp(self):
        file_with_logs = open('dummy_logs', 'r')
        # see dummy_logs to know if unrelated_line and system_line are as named
        self.unrelated_line = file_with_logs.readline()
        self.system_line = file_with_logs.readline()
        self.unrelated_log = data.log.Log(self.unrelated_line)
        self.system_log = data.log.Log(self.system_line)

        self._expected_parts = [
            {"name": "Modules",
             "value": u"BinModule1"},
            {"name": "File",
             "value": u"bin\\binmodule1\\utils.cpp"},
            {"name": "Function",
             "value": u"sum"},
            {"name": "Message",
             "value": u"1: Some message from the system from binary module 1\n "}
        ]

    def test_unrelated_log(self):
        parser = logger_configuration.CONFIGURATION["parser"]
        parts = parser["parts"]

        for part in parts:
            name = part["name"]
            part_of_log = self.unrelated_log.get_part(name)
            if name != 'Message':
                self.assertEqual(part_of_log, '')
            else:
                self.assertEqual(part_of_log, self.unrelated_line)

    def test_log_from_the_system(self):

        for part in self._expected_parts:
            name = part["name"]
            part_of_log = self.system_log.get_part(name)
            self.assertEqual(part_of_log, part["value"])


suite = unittest.TestLoader().loadTestsFromTestCase(LogTests)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)