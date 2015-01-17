__author__ = 'twyrwas'

import unittest
import ui_utilities.exceptions


class FakeUI:

    def __init__(self):
        self._notified = False
        self._terminated = None
        self._message = None

    def notify_exception(self, message, terminate):
        self._notified = True
        self._terminated = terminate
        self._message = message

    def reset(self):
        self._notified = False
        self._terminated = None
        self._message = None

    def was_notified(self):
        return self._notified

    def was_terminated(self):
        return self._terminated

    def get_message(self):
        return self._message


class NotifierTests(unittest.TestCase):

    def test_notification_flow(self):

        ui = FakeUI()
        ui_utilities.exceptions.Notifier.register_ui(ui)
        ui_utilities.exceptions.Notifier.push('Some exception happened!', False)

        self.assertTrue(ui.was_notified())
        self.assertFalse(ui.was_terminated())
        self.assertEqual(ui.get_message(), 'Some exception happened!')

        ui.reset()

        ui_utilities.exceptions.Notifier.push('Some fatal exception happened!', True)

        self.assertTrue(ui.was_notified())
        self.assertTrue(ui.was_terminated())
        self.assertEqual(ui.get_message(), 'Some fatal exception happened!')


suite = unittest.TestLoader().loadTestsFromTestCase(NotifierTests)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)