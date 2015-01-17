__author__ = 'twyrwas'


class Notifier:

    _instance = None

    @classmethod
    def register_ui(cls, ui):
        cls._instance = Notifier(ui)

    @classmethod
    def push(cls, message='Fatal exception!', terminate=True):
        if cls._instance is not None:
            cls._instance.notify_ui(message, terminate)
        else:
            print 'Exception Notifier: No UI registered!'

    def __init__(self, ui):
        self._ui = ui

    def notify_ui(self, message, terminate):
        self._ui.notify_exception(message, terminate)