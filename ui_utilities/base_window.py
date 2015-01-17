__author__ = 'twyrwas'


class BaseWindow:
    """ Base class for main window.
    """

    def get_model(self):
        pass

    def notify_new_logs(self):
        pass

    def filtering_changed(self):
        pass

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

    def notify_exception(self, message, terminate):
        pass

