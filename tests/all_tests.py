__author__ = 'twyrwas'

import unittest
import log_tests
import logs_container_tests
import keeper_tests
import layout_reader_tests
import input_history_tests
import exception_notifier_tests

suites = (log_tests.suite, logs_container_tests.suite, keeper_tests.suite, layout_reader_tests.suite,
          input_history_tests.suite, exception_notifier_tests.suite)
all_tests_suite = unittest.TestSuite(suites)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(all_tests_suite)