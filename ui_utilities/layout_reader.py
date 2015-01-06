import logger_configuration


class LayoutReader:

    def __init__(self):
        parser = logger_configuration.CONFIGURATION['parser']
        parts = parser['parts']
        self._filter_options = dict()
        self._parts = list()
        self._read_filter_options(parts)
        self._read_parts(parts)

    def get_filter_options(self):
        return self._filter_options

    def get_parts(self):
        return self._parts

    def _read_filter_options(self, parts):
        for part in parts:
            classifications = part.get('classifications', False)
            if classifications:
                for cl in classifications:
                    name = cl['class']
                    self._filter_options[name] = cl['pattern']
                break

    def _read_parts(self, parts):
        for part in parts:
            name = part['name']
            self._parts.append(name)