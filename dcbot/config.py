import configparser
import sys


class Config:
    def __init__(self, config_file='config/config.ini'):
        self.config_file = config_file
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        self.token = config.get('Credentials', 'Token', fallback=None)
        self.activator_left, self.activator_right = config.get('Activator', 'Activator', fallback='[$]').split('$')
        self.command_trigger = config.get('Commands', 'CommandTrigger', fallback='!')
        self.debug = config.get('Debug', 'Debug', fallback=False) in ['True']
        self.use_inven = config.get('Other', 'UseInven', fallback=False) in ['True']

        if not self.token:
            print("TOKEN UNSET, exiting now", file=sys.stderr)
            sys.exit()
