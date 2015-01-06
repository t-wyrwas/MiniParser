__author__ = 'twyrwas'
import ui_utilities.layout_reader
import unittest


class LayoutReaderTests(unittest.TestCase):

    def setUp(self):
        self._l_reader = ui_utilities.layout_reader.LayoutReader()
        self._expected_filter_options = {u'LibModule1': u'lib\\libmodule1', u'BinModule1': u'bin\\binmodule1',
                                         u'LibModule2': u'lib\\libmodule2'}
        self._expected_parts = [u'Modules', u'File', u'Message', u'Function']

    def test_get_filter_options(self):
        filter_options = self._l_reader.get_filter_options()
        self.assertEqual(len(filter_options), len(self._expected_filter_options))
        for option in filter_options:
            self.assertEqual(filter_options[option], self._expected_filter_options[option])

    def test_get_parts(self):
        parts = self._l_reader.get_parts()
        self.assertEqual(len(parts), len(self._expected_parts))
        pairs_to_check = zip(parts, self._expected_parts)
        for (part, expected_part) in pairs_to_check:
            self.assertEqual(part, expected_part)
        self.assertEqual(type(parts[0]), unicode)


suite = unittest.TestLoader().loadTestsFromTestCase(LayoutReaderTests)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)