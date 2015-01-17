import threading
import time
import os

import wx

import ui_utilities.input_history
import ui_utilities.user_filter
import ui_utilities.base_window
import ui_utilities.layout_reader

import data.keeper

import communication.file_read
import communication.serial_port_reader
import logger_configuration

import ui_utilities.exceptions



# TODO define names of modules in one place
# TODO think about better design to make adding new check box quicker

ID_SERIAL_PORT_OPEN = 8001
ID_SERIAL_PORT_CLOSE = 8002
ID_QUICK_SAVE = 8003
ID_QUICK_SAVE_FILTERED = 8004


#todo make it inherit from general interface to create abstraction layer between wx and the rest of code
class WxMainWindow (ui_utilities.base_window.BaseWindow, wx.Frame):

    def __init__(self, *args, **kwargs):
        super(WxMainWindow, self).__init__(*args, **kwargs)

        ui_utilities.exceptions.Notifier.register_ui(self)

        self._model = data.keeper.Keeper(self)
        self._logs_to_display = []
        self._prev_log = str()
        self._index = 0
        self._reader = communication.file_read.FileReader(self._model, '')    #todo refactor
        self._serial_port_reader = communication.serial_port_reader.SerialPortReader(self._model) # wtf?

        self.COLOUR_MARK = wx.Colour(200, 200, 250)
        self.COLOUR_DOUBLE_MARK = wx.Colour(100, 100, 250)
        self.COLOUR_UNMARK = wx.Colour(255, 255, 255)
        self._INFO_LABELS = dict()
        self._set_info_labels()

        menu_bar = wx.MenuBar()
        # File Menu
        file_menu = wx.Menu()
        clear_display_item = file_menu.Append(wx.ID_CLEAR, 'Clear display', 'Clear display')
        file_menu.Bind(wx.EVT_MENU, self._on_clear_display, clear_display_item)
        # Read file
        open_item = file_menu.Append(wx.ID_OPEN, 'Open', 'Open file')
        file_menu.Bind(wx.EVT_MENU, self._on_read, open_item)
        # Quick save
        quick_save_item = file_menu.Append(ID_QUICK_SAVE, 'Quick save', 'Save to default file')
        file_menu.Bind(wx.EVT_MENU, self._on_quick_save, quick_save_item)
        # Quick save filtered
        quick_save_filtered_item = file_menu.Append(ID_QUICK_SAVE_FILTERED, 'Quick save filtered', 'Save filtered logs to default file')
        file_menu.Bind(wx.EVT_MENU, self._on_quick_save_filtered, quick_save_filtered_item)
        # Save file
        save_item = file_menu.Append(wx.ID_SAVE, 'Save', 'Save dump to file')
        file_menu.Bind(wx.EVT_MENU, self._on_save, save_item)
        # Save filtered dump
        save_filtered_item = file_menu.Append(wx.ID_SAVE, 'Save filtered', 'Save filtered dump (displayed only)')
        file_menu.Bind(wx.EVT_MENU, self._on_save_filtered, save_filtered_item)
        # Quit
        quit_item = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        file_menu.Bind(wx.EVT_MENU, self._on_quit, quit_item)
        menu_bar.Append(file_menu, '&File')

        # Comm menu
        comm_menu = wx.Menu()
        # Read from serial port
        read_ser_port_item = comm_menu.Append(ID_SERIAL_PORT_OPEN, 'Read serial port', 'Read dump from serial port')
        comm_menu.Bind(wx.EVT_MENU, self._on_read_ser_port, read_ser_port_item)
        # Stop reading from serial port
        stop_ser_port_item = comm_menu.Append(ID_SERIAL_PORT_CLOSE, 'Stop serial port', 'Stop reading from serial port')
        comm_menu.Bind(wx.EVT_MENU, self._on_stop_ser_port, stop_ser_port_item)
        menu_bar.Append(comm_menu, '&Comm')

        # Status bar
        self._status_bar = self.CreateStatusBar()
        self._status_view = str()

        # View Menu - check boxes
        view_menu = wx.Menu()
        l_reader = ui_utilities.layout_reader.LayoutReader()
        filter_options = l_reader.get_filter_options()
        self._filter_options = dict()
        for filter_option in filter_options.keys():
            self._filter_options[filter_option] = view_menu.Append(wx.ID_ANY, filter_option, filter_option, wx.ITEM_CHECK)
            view_menu.Bind(wx.EVT_MENU, self._toggle_filter_checkbox, self._filter_options[filter_option])
        #todo Unknown and Other should probably go to logger_configuration.CONFIGURATION
        self._filter_options["Unknown"] = view_menu.Append(wx.ID_ANY, "Unknown", "Unknown", wx.ITEM_CHECK)
        view_menu.Bind(wx.EVT_MENU, self._toggle_filter_checkbox, self._filter_options["Unknown"])
        self._filter_options["Other"] = view_menu.Append(wx.ID_ANY, "Other", "Other", wx.ITEM_CHECK)
        view_menu.Bind(wx.EVT_MENU, self._toggle_filter_checkbox, self._filter_options["Other"])

        menu_bar.Append(view_menu, '&View')
        self.SetMenuBar(menu_bar)

        # Panel
        self._panel = wx.Panel(self)
        self._box_sizer = wx.BoxSizer(wx.VERTICAL)
        # Display
        self._columns = l_reader.get_parts()
        rev_columns = list(self._columns)
        rev_columns.reverse()
        self._display = wx.ListCtrl(self._panel, size=(-1, 100), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        for column in rev_columns:
            self._display.InsertColumn(0, column, width=100)
        self._display.DeleteAllItems()
        self._box_sizer.Add(self._display, 1, wx.ALL | wx.EXPAND, 8)
        self._panel.SetSizer(self._box_sizer)
        self.filtering_changed()

        # User filter field
        self._text = wx.TextCtrl(self._panel, size=(1, 20), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)
        self._box_sizer.Add(self._text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        # Event
        self._text.Bind(wx.EVT_KEY_DOWN, self._on_key_down_text)
        # User filter object
        self._user_filter = ui_utilities.user_filter.UserFilter(self)
        self._user_input_history = ui_utilities.input_history.InputHistory()

        # Frame
        frame_size = logger_configuration.CONFIGURATION['size']
        self.SetSize((frame_size['width'], frame_size['height']))
        self._set_title()
        self.Center()
        self.Show()

        # Release what's necessary
        self.Bind(wx.EVT_CLOSE, self._on_closed)

    def get_model(self):
        return self._model

    def filtering_changed(self):
        self._clear_display()
        filter = self._model.get_filter_values()
        for checkbox_name in self._filter_options:
            checkbox = self._filter_options[checkbox_name]
            checkbox.Check(filter[checkbox.GetText()])
        self._status_view = str(self._model)
        self._update_status_bar()
        self._intercept_new_logs()

    def notify_new_logs(self):
        self._intercept_new_logs()

    def _set_title(self, info = ''):
        whole_title = self._INFO_LABELS['TITLE']
        if info != '':
            whole_title += ' - '
            whole_title += info
        self.SetTitle(whole_title)

    def _set_info_labels(self):
        self._INFO_LABELS['TITLE'] = 'MiniParser'
        self._INFO_LABELS['SERIAL_PORT_READ'] = 'Reading from serial port'

    def _clear_display(self):
        self._display.DeleteAllItems()
        self._index = 0
        self._logs_to_display = []
        # todo creating new UserFilter - maybe implement reset method?
        self._user_filter = ui_utilities.user_filter.UserFilter(self)

    def _reset(self):
        self._clear_display()
        self._model.reset()
        self._update_status_bar()
        self._set_title()

    def _intercept_new_logs(self):
        new_logs = self._model.get_new_logs()
        self._logs_to_display += new_logs
        self._display_logs(new_logs)

    def _display_logs(self, logs):
        for log in logs:
            self._display.InsertStringItem(self._index, log.get_part(self._columns[0]))
            column_index = 1
            for column in self._columns[1:]:
                self._display.SetStringItem(self._index, column_index, log.get_part(column))
                column_index += 1
            self._index += 1
        self._update_status_bar()

    def get_item(self, i):
        return self._display.GetItemText(i, 2)

    def get_item_count(self):
        return self._display.GetItemCount()

    def mark_item(self, item_index):
        self._display.SetItemBackgroundColour(item_index, self.COLOUR_MARK)

    def double_mark_item(self, item_index):
        self._display.SetItemBackgroundColour(item_index, self.COLOUR_DOUBLE_MARK)
        self._display.EnsureVisible(item_index)

    def unmark_item(self, item_index):
        self._display.SetItemBackgroundColour(item_index, self.COLOUR_UNMARK)

    def notify_exception(self, message, terminate):
        wx.MessageBox(message, 'Exception!', wx.OK | wx.ICON_ERROR)
        self._on_quit(None)

#todo think of a better way to handle status bar
    def _update_status_bar(self, additional_info=None):
        separator = ' | '
        count_info = str(len(self._logs_to_display)) + ' lines displayed'
        status = self._status_view + separator + count_info
        addition = ''
        if additional_info is not None:
            for key in additional_info:
                addition += str(key) + ': ' + str(additional_info[key])
            status += separator + addition
        self._status_bar.SetStatusText(status)

    def _on_quit(self, e):
        self.Close()

    def _on_closed(self, e):
        # self._serial_port_reader.stop() #todo doesn't work
        self._reader.stop()
        self.Destroy()

    def _on_clear_display(self, e):
        self._reset()

    def _on_read(self, e):
        self._reader.stop()
        dialog = wx.FileDialog(self, 'Open', '', r'C:\\', 'All (*)|*', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            self._reset()
            #todo refactor
            self._clear_display()
            filter = self._model.get_filter_values()
            for checkbox_name in self._filter_options:
                checkbox = self._filter_options[checkbox_name]
                checkbox.Check(filter[checkbox.GetText()])
            self._status_view = str(self._model)
            self._update_status_bar()
            path = dialog.GetPath()
            self._set_title(path)
            dialog.Destroy()
            self._reader = communication.file_read.FileReader(self.get_model(), path)
            reader_thread = threading.Thread(target=self._reader.run)
            reader_thread.start()

    def _on_read_ser_port(self, e):
        self._serial_port_reader.stop()
        self._reader.stop()
        reader_thread = threading.Thread(target=self._serial_port_reader.run)
        reader_thread.start()
        self._set_title(self._INFO_LABELS['SERIAL_PORT_READ'])

    def _on_stop_ser_port(self, e):
        self._serial_port_reader.stop()
        self._set_title()

    def _on_save(self, e):
        #todo
        pass

    #todo quick saves will save empty files - need to be handled
    def _on_quick_save(self, e):
        default_file = self._open_default_file()
        for log in self._model.all_logs():
            default_file.write(str(log))
        default_file.close()

    def _on_quick_save_filtered(self, e):
        default_file = self._open_default_file()
        for log in self._logs_to_display:
            default_file.write(str(log))
        default_file.close()

    def _open_default_file(self):
        sec_from_epoch = time.time()
        full_time = time.gmtime(sec_from_epoch)
        filename = 'MINI_PARSER_LOGS_'
        filename += str(full_time[0]) + '-' + str(full_time[1]) + '-' + str(full_time[2]) + '_' \
                   + str(full_time[3]) + '-' + str(full_time[4]) + '-' + str(full_time[5])
        path = filename

        destination = logger_configuration.CONFIGURATION['default_path']
        if destination is not '':
            if os.path.exists(destination) is not True:
                os.makedirs(destination)
            path = destination + '\\' + filename    #todo whether we use / or \ should be dependant on type of OS

        return open(path, 'w')

    def _on_save_filtered(self, e):
        #todo
        pass

    def _on_key_down_text(self, e):
        if e.GetKeyCode() == wx.WXK_RETURN:
            reverse_order = e.ShiftDown()
            user_input = self._text.GetValue()
            self._user_filter.update_user_filter(user_input, reverse_order)
            if user_input != '':
                self._user_input_history.add(user_input)
        if e.GetKeyCode() == wx.WXK_ESCAPE:
            self._user_filter.update_user_filter('', False)
            self._text.Clear()
            self._user_input_history.reset_index()
            self._update_status_bar()
        if e.GetKeyCode() == wx.WXK_UP:
            prev_input = self._user_input_history.get_previous_input()
            self._text.SetValue(prev_input)
        if e.GetKeyCode() == wx.WXK_DOWN:
            next_input = self._user_input_history.get_next_input()
            self._text.SetValue(next_input)
        else:
            e.Skip()

    def _toggle_filter_checkbox(self, e):
        new_filtering = dict()
        for checkbox_name in self._filter_options:
            checkbox = self._filter_options[checkbox_name]
            if checkbox.IsChecked():
                new_filtering[checkbox_name] = True
            else:
                new_filtering[checkbox_name] = False
        self._model.update_filter(new_filtering)