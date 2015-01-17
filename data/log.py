import logger_configuration
from ui_utilities.exceptions import Notifier as ExpNotifier


class Log:

    """ Class to store a single log. """

    def __init__(self, message):

        self._text_repr = message
        parser = logger_configuration.CONFIGURATION["parser"]
        parts = parser["parts"]
        self._parts_of_message = dict()
        log_is_unrelated = False

        try:
            signature = parser["logs_signature"]

            if signature["value"] not in message:   #todo take position into consideration
                log_is_unrelated = True

            for part in parts:

                name = part["name"]

                if log_is_unrelated:
                    if part.get("for_unrelated", False):
                        part_of_message = self._text_repr
                    else:
                        part_of_message = ''
                else:
                    classifications = part.get("classifications", False)
                    if classifications:
                        part_of_message = self._parse_by_classifications(classifications, message)
                    else:
                        part_of_message = self._parse_by_position(message, parser["separator"], part.get("start"), part.get("end"))

                self._parts_of_message[name] = part_of_message

        except KeyError:
            ExpNotifier.push('Configuration file is corrupted!')

    def get_part(self, name):
        try:
            part = self._parts_of_message[name]
        except KeyError:
            ExpNotifier.push('No specified part of log!')
        else:
            return part

    def get_whole(self):
        return self._text_repr

    @staticmethod
    def _parse_by_classifications(classifications, message):

        part_of_message = "Unknown"
        for cl in classifications:
            if cl["pattern"] in message:
                part_of_message = cl["class"]
                break
        return part_of_message

    @staticmethod
    def _parse_by_position(message, separator, start_pos, end_pos):

        msg_splitted = message.split(separator)
        if start_pos == end_pos:
            part_of_message = msg_splitted[start_pos]
        if end_pos < 0:
            parts_to_take = msg_splitted[start_pos:len(msg_splitted)]
            combined = str()
            for p in parts_to_take:
                combined += p
                combined += separator
            part_of_message = combined

        return part_of_message

    def __str__(self):
        return self._text_repr