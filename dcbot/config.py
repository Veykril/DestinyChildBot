import configparser
import sys


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        self.token = config.get('Credentials', 'Token', fallback=None)
        self.trigger = config.get('Commands', 'Trigger', fallback='!')
        self.command_trigger = config.get('Commands', 'CommandTrigger', fallback='~')
        self.lextender = config.get('Commands', 'L-Extender', fallback='"')
        self.rextender = config.get('Commands', 'R-Extender', fallback='"')
        self.debug = config.get('Debug', 'debug', fallback=False) in ["True"]

        if self.token is None:
            print("TOKEN UNSET, exiting now", file=sys.stderr)
            sys.exit()
