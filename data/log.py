import logger_configuration


class Log:

    """ Class to store a single log. """

    def __init__(self, message):
        self._text_repr = message
        parser = logger_configuration.CONFIGURATION["parser"]
        self._parts_of_message = dict()
        unrelated = False
        signature = parser["logs_signature"]

        if signature["value"] not in message:   #todo take position into consideration
            unrelated = True

        for part in parser["parts"]:
            name = part["name"]
            part_of_message = str()

            if unrelated is True:
                if part.get("for_unrelated", False):
                    part_of_message = self._text_repr
                else:
                    part_of_message = ''
            else:
                classifications = part.get("classifications", False)

                if classifications:
                    part_of_message = "Unknown"
                    for clssif in classifications:
                        if clssif["pattern"] in message:
                            part_of_message = clssif["class"]
                            break
                else:
                    separator = parser["separator"]
                    start_pos = part.get("start")
                    end_pos = part.get("end")
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
                    #todo check agains unwanted start_pos, end_pos values

            self._parts_of_message[name] = part_of_message

    def get_part(self, name):
        return self._parts_of_message[name]

    def get_whole(self):
        return self._text_repr

    def __str__(self):
        return self._text_repr