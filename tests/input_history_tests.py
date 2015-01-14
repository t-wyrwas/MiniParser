__author__ = 'twyrwas'

import unittest
import ui_utilities.input_history


class InputHistoryTests(unittest.TestCase):

    def setUp(self):
        self._cmds = ['first command', 'second command', 'third command', 'fourth command', 'fifth command']
        self._history = ui_utilities.input_history.InputHistory()
        for command in self._cmds:
            self._history.add(command)

    def test_get_previous_and_next_input(self):

        self._cmds.reverse()

        for command in self._cmds[1:len(self._cmds)]:
            self.assertEqual(command, self._history.get_previous_input())

        self._cmds.reverse()

        for command in self._cmds[1: len(self._cmds)]:
            self.assertEqual(command, self._history.get_next_input())

    def test_reset_index(self):

        last_cmd = len(self._cmds) - 1
        self.assertEqual(self._cmds[last_cmd-1], self._history.get_previous_input())
        self.assertEqual(self._cmds[last_cmd-2], self._history.get_previous_input())
        self._history.reset_index()
        self.assertEqual(self._cmds[last_cmd-1], self._history.get_previous_input())

    def test_boundaries(self):

        for i in range(0, 2*len(self._cmds)):
            self._history.get_previous_input()

        self.assertEqual(self._cmds[0], self._history.get_previous_input())

        for i in range(0, 2*len(self._cmds)):
            self._history.get_next_input()

        self.assertEqual(self._cmds[len(self._cmds)-1], self._history.get_next_input())


suite = unittest.TestLoader().loadTestsFromTestCase(InputHistoryTests)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)