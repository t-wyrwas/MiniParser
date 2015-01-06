__author__ = 'twyrwas'


class UserFilter:

    def __init__(self, window):
        self._window = window
        self._user_filter = None
        self._current_position_index = -2
        self._prev_user_filter = None
        self._all_found_positions = []

    def __call__(self, log):
        if self._user_filter is not None:
            if self._user_filter in log:
                return True
            else:
                return False
        return True

    def update_user_filter(self, text, reverse_order):
        if text == '':
            self._clear_filter()
            return
        if text == self._prev_user_filter:
            self._update_position(reverse_order)
        else:
            self._clear_filter()
            self._user_filter = text
            self._mark_filtered_items()

    def _update_position(self, reverse_order):
        if len(self._all_found_positions) is 0:
            return
        if reverse_order:
            self._reverse_position()
        else:
            self._forward_position()

    def _reverse_position(self):
        position_count = len(self._all_found_positions)
        if self._current_position_index == -2:  # -2 means that this is the first user attempt double mark position
            self._current_position_index = 0
        else:
            self._current_position_index -= 1
            if self._current_position_index < 0:
                self._current_position_index = position_count - 1

        if position_count > 1:
            prev_pos = None
            next_pos = None
            if self._current_position_index == 0:
                prev_pos = 1
                next_pos = position_count-1
            elif self._current_position_index == position_count-1:
                prev_pos = 0
                next_pos = position_count-2
            else:
                prev_pos = self._current_position_index + 1
                next_pos = self._current_position_index - 1
            # normal mark for both previous and next positions (in case forward positioning was made before)
            item_index = self._all_found_positions[prev_pos]
            self._window.mark_item(item_index)
            item_index = self._all_found_positions[next_pos]
            self._window.mark_item(item_index)
        # double mark for current position
        item_index = self._all_found_positions[self._current_position_index]
        self._window.double_mark_item(item_index)

    def _forward_position(self):
        position_count = len(self._all_found_positions)
        if self._current_position_index == -2:  # -2 means that this is the first user attempt double mark position
            self._current_position_index = 0
        else:
            self._current_position_index += 1
            if self._current_position_index > position_count - 1:
                self._current_position_index = 0
        prev_pos = None
        next_pos = None
        if self._current_position_index == 0:
            prev_pos = position_count - 1
            next_pos = 1
        if self._current_position_index == position_count-1:
            prev_pos = position_count - 2
            next_pos = 0
        else:
            prev_pos = self._current_position_index - 1
            next_pos = self._current_position_index + 1
        # normal mark for both previous and next positions (in case reverse positioning was made before)
        item_index = self._all_found_positions[prev_pos]
        self._window.mark_item(item_index)
        item_index = self._all_found_positions[next_pos]
        self._window.mark_item(item_index)
        # double mark for current position
        item_index = self._all_found_positions[self._current_position_index]
        self._window.double_mark_item(item_index)

    def _mark_filtered_items(self):
        i = 0
        self._prev_user_filter = self._user_filter
        count = self._window.get_item_count()
        while i < count:
            msg = self._window.get_item(i)
            if self(msg):
                self._window.mark_item(i)
                self._all_found_positions.append(i)
            i += 1
        self._window._update_status_bar({'Found': len(self._all_found_positions)})

    def _clear_filter(self):
        for item_index in self._all_found_positions:
            self._window.unmark_item(item_index)
        self._user_filter = None
        self._prev_user_filter = None
        self._all_found_positions = []
        self._current_position_index = -2
