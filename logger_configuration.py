__author__ = 'twyrwas'
import json
import os.path

_CONFIGURATION_FILE = 'logger_configuration.json'

_DEFAULT_CONFIGURATION = {

    "default_path": "C:\\MINIMALIST_PARSER_LOGS",

    "size": {"width": 1024, "height": 720},

    "parser": {

        "separator": " ",

        "logs_signature": {
            "value": "TEST_SIG",
            "position": 0
        },

        "parts": [
            {"name": "Modules",
                "classifications": [
                    {"pattern": "bin\\binmodule1",
                        "class": "BinModule1"},
                    {"pattern": "lib\\libmodule1",
                        "class": "LibModule1"},
                    {"pattern": "lib\\libmodule2",
                        "class": "LibModule2"}],
                "filter": 1},

            {"name": "File",
                "start": 1,
                "end": 1},

            {"name": "Message",
                "start": 3,
                "end": -1,
                "for_unrelated": 1},

            {"name": "Function",
                "start": 2,
                "end": 2}
        ]
    }
}

CONFIGURATION = _DEFAULT_CONFIGURATION

if os.path.isfile(_CONFIGURATION_FILE):
    config = json.load(open(_CONFIGURATION_FILE))
    CONFIGURATION = config
else:
    json.dump(_DEFAULT_CONFIGURATION, open(_CONFIGURATION_FILE, 'w'))