__author__ = 'twyrwas'


class InputHistory:

    def __init__(self):
        self._history = list()
        self._index = 0

    def get_previous_input(self):
        history_size = len(self._history)
        if history_size == 0:
            return ''
        if self._index != 0:
            self._index -= 1
        return self._history[self._index]

    def get_next_input(self):
        history_size = len(self._history)
        if history_size == 0:
            return ''
        if self._index < history_size - 1:
            self._index += 1
        return self._history[self._index]

    def reset_index(self):
        self._index = len(self._history) - 1

    def add(self, input_to_archive):
        self.reset_index()
        if len(self._history) > 0:
            prev_input = self._history[len(self._history)-1]
            if input_to_archive == prev_input:
                return
        self._history.append(input_to_archive)
        self.reset_index()
