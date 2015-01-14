__author__ = 'twyrwas'

import unittest
import data.keeper
import data.log
from ui_utilities.base_window import BaseWindow


class DummyWindow(BaseWindow):

    """ Keeper invokes two methods of BaseWindow:
    - filtering_changed
    - notify_new_logs
    """

    def __init__(self):
        self.methods_invoked = dict()
        self.reset()

    def get_model(self):
        pass

    def notify_new_logs(self):
        self.methods_invoked["notify_new_logs"] = True

    def filtering_changed(self):
        self.methods_invoked["filtering_changed"] = True

    def get_item(self, i):
        pass

    def get_item_count(self):
        pass

    def mark_item(self, item_index):
        pass

    def double_mark_item(self, item_index):
        pass

    def unmark_item(self, item_index):
        pass

    def reset(self):
        self.methods_invoked["filtering_changed"] = False
        self.methods_invoked["notify_new_logs"] = False


class KeeperTests(unittest.TestCase):

    def setUp(self):
        logs_file = open('dummy_logs', 'r')
        self._expected_logs = list()
        line = logs_file.readline()
        self._dummy_window = DummyWindow()
        self._keeper = data.keeper.Keeper(self._dummy_window)
        while line:
            log = data.log.Log(line)
            self._expected_logs.append(log)
            self._keeper.append(line)
            line = logs_file.readline()

    def test_all_logs(self):
        i = 0
        for log in self._keeper.all_logs():
            self.assertEqual(log.get_whole(), self._expected_logs[i].get_whole())
            i += 1

    def test_get_new_logs(self):
        logs_to_append = ['some random new_log', 'some random new_log1', 'some random new_log2']
        new_logs = self._keeper.get_new_logs()
        self.assertEqual(len(new_logs), len(self._expected_logs))
        return
        i = 0
        for log in new_logs:
            self.assertEqual(log.get_whole(), self._expected_logs[i].get_whole())
            i += 1

        for line in logs_to_append:
            self._keeper.append(line)
        new_logs = self._keeper.get_new_logs()
        self.assertEqual(len(new_logs), len(logs_to_append))

        self._keeper.update_filter(dict())
        new_logs = self._keeper.get_new_logs()
        self.assertEqual(len(new_logs), len(self._expected_logs) + 3)
        new_logs = self._keeper.get_new_logs()
        self.assertEqual(len(new_logs), 0)
        self._keeper.append(logs_to_append[0])
        new_logs = self._keeper.get_new_logs()
        self.assertEqual(len(new_logs), 1)

    def test_notify_new_logs(self):
        self._dummy_window.reset()
        self.assertFalse(self._dummy_window.methods_invoked['notify_new_logs'])
        self._keeper.append('some random new log')
        self.assertTrue(self._dummy_window.methods_invoked['notify_new_logs'])

    def test_filtering_changed(self):
        self._dummy_window.reset()
        self.assertFalse(self._dummy_window.methods_invoked['filtering_changed'])
        self._keeper.append('some random new log')
        self.assertFalse(self._dummy_window.methods_invoked['filtering_changed'])
        self._keeper.update_filter(dict())
        self.assertTrue(self._dummy_window.methods_invoked['filtering_changed'])

    def test_get_filter_values(self):
        expected_filter = {u'LibModule1': True, u'Unknown': True, u'BinModule1': True, u'LibModule2': True, u'Other': True}
        filter_values = self._keeper.get_filter_values()
        self.assertEqual(len(filter_values), len(expected_filter))

        filter_keys = filter_values.keys()
        expected_filter_keys = expected_filter.keys()

        for key in filter_keys:
            self.assertTrue(key in expected_filter_keys)

        for module in filter_values:
            self.assertEqual(filter_values[module], expected_filter[module])

    def test_update_filter_values(self):
        original_filter = {u'LibModule1': True, u'Unknown': True, u'BinModule1': True, u'LibModule2': True, u'Other': True}
        new_filter_values = {'ThridPartyModule1': True, 'BrandNewLibModule1': True, 'ReallyDisturbingModule': False}
        self._keeper.update_filter(new_filter_values)
        filter_values = self._keeper.get_filter_values()

        self.assertEqual(len(filter_values), len(original_filter) + len(new_filter_values))

        for key in original_filter:
            self.assertTrue(key in filter_values.keys())
            self.assertEqual(original_filter[key], filter_values[key])

        for key in new_filter_values:
            self.assertTrue(key in filter_values.keys())
            self.assertEqual(new_filter_values[key], filter_values[key])


suite = unittest.TestLoader().loadTestsFromTestCase(KeeperTests)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)