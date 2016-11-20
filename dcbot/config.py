import configparser


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        self.token = config.get('Credentials', 'Token', fallback=None)
        self.trigger = config.get('Commands', 'Trigger', fallback=None)
        self.command_trigger = config.get('Commands', 'CommandTrigger', fallback=None)
        self.lextender = config.get('Commands', 'L-Extender', fallback=None)
        self.rextender = config.get('Commands', 'R-Extender', fallback=None)
        self.debug = bool(config.get('Debug', 'debug', fallback=None))
