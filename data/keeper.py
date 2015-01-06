__author__ = 'twyrwas'

from data import logs_container
import data.log
import logger_configuration


class Keeper:

    """ Data model class which handles not only the filtering options but also log container and
    notifications to panel (view).
    TODO:
    - Currently only one-dimension filtering is supported (only first found classification
    denoted as input for filter is considered).
    - Log instances are not internal for Keeper. They are used throughout the code - shouldn't Log class be hidden outside Keeper?
    """

    def __init__(self, window):
        self._window = window
        self._logs_container = logs_container.LogsContainer()
        self._new_logs_marker = 0
        self._filter_values = dict()
        self._filter_patterns = dict()
        self._filtered_part_name = None
        self._set_filtering()

    def get_new_logs(self):
        new_logs = self._logs_container[self._new_logs_marker:]
        new_logs = self._filter(new_logs)
        self._new_logs_marker += len(new_logs)
        return new_logs

    #todo is it the best way?
    def all_logs(self):
        for log in self._logs_container:
            yield log

    def update_filter(self, new_filtering):
        self._filter_values.update(new_filtering)
        self._new_logs_marker = 0
        self._window.filtering_changed()

    #todo should probably return whole dictionary of filter values
    def get_filter_values(self):
        return self._filter_values

    def append(self, line):
        log = data.log.Log(line)
        self._logs_container.append(log)
        self._window.notify_new_logs()

    def reset(self):
        self._logs_container = logs_container.LogsContainer()
        self._new_logs_marker = 0
        for key in self._filter_values:
            self._filter_values[key] = True

    def _set_filtering(self):
        parser = logger_configuration.CONFIGURATION['parser']
        list_of_parts = parser['parts']
        for part in list_of_parts:
            classifications = part.get("classifications", False)
            if classifications:
                self._filtered_part_name = part['name']
                for classification in classifications:
                    class_name = classification['class']
                    pattern = classification['pattern']
                    self._filter_values[class_name] = True
                    self._filter_patterns[class_name] = pattern
                self._filter_values['Unknown'] = True
                self._filter_values['Other'] = True
                break

    def _filter(self, logs):
        filtered_logs = []
        for log in logs:
            log_class_name = log.get_part(self._filtered_part_name)
            if log_class_name is '':
                if self._filter_values['Other']:
                    filtered_logs.append(log)
            else:
                for class_name in self._filter_values:
                    class_passes = self._filter_values[class_name]
                    log_in_class = log_class_name is class_name
                    if log_in_class and class_passes:
                        filtered_logs.append(log)
                        break

        # for log in logs:
        #     for class_name in self._filter_values:
        #         class_passes = self._filter_values[class_name]
        #         log_class_name = log.get_part(self._filtered_part_name)
        #         log_is_from_class = log_class_name == class_name
        #         if class_passes and log_is_from_class:
        #             print 'YES', log.get_whole()
        #             filtered_logs.append(log)
        #         else:
        #             print 'NO', log.get_whole()

        # print 'filtered_logs'
        # for log in filtered_logs:
        #     print log.get_whole()
        return filtered_logs

#todo change to standard method to enhance readability
    def __str__(self):
        return_str = 'View: '
        view_all = True
        for module_name in self._filter_values:
            if self._filter_values[module_name] == False:
                view_all = False
                break

        if view_all:
            return_str += 'all'
            return return_str

        for module_name in self._filter_values:
            if self._filter_values[module_name]:
                return_str += module_name
                return_str += ' '

        return return_str