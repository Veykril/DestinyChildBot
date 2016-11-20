import asyncio

from dcbot.config import Config
from dcbot.jsonhelper import JSONHelper
from dcbot.child import Element
from dcbot.child import Role
from dcbot.constants import *

import discord

import traceback


class DestinyChildBot(discord.Client):
    def __init__(self, config_file='Config/config.ini'):
        self.config = Config(config_file)
        self.json = JSONHelper("resources/children.json")
        super().__init__()

    def run(self):
        super().run(self.config.token)

    async def on_error(self, event, *args, **kwargs):
        traceback.print_exc()

    async def on_ready(self):
        print("Successfully connected!")

    async def on_message(self, message):
        print("[{}]@{}:{}".format(message.server, message.channel, message.content))
        if message.author == self.user:
            return

        content = message.content.strip()  # type: str

        if content.startswith(self.config.command_trigger):  # THIS WILL LOOK UGLY AF since it is just a temporary thing for adding chidlren to the json file
            command, *args = content.split()
            command = command[len(self.config.command_trigger):].lower().strip()

            cmd_func = getattr(self, 'c_{}'.format(command))

            if command == "create_child_entry":
                func_kwargs = {}
                func_kwargs[JSON_IDX] = int(args[0])
                func_kwargs[JSON_ID] = int(args[1])
                func_kwargs[JSON_INVEN_ID] = int(args[2])
                func_kwargs[JSON_NAME] = args[3]
                func_kwargs[JSON_EN_NAME] = args[4]
                func_kwargs[JSON_RARITY] = int(args[5])
                func_kwargs[JSON_ELEMENT] = Element[args[6].lower()].value
                func_kwargs[JSON_ROLE] = Role[args[7].lower()].value
                func_kwargs[JSON_STAT_HP] = int(args[8])
                func_kwargs[JSON_STAT_ATK] = int(args[9])
                func_kwargs[JSON_STAT_DEF] = int(args[10])
                func_kwargs[JSON_STAT_AGI] = int(args[11])
                func_kwargs[JSON_STAT_CRIT] = int(args[12])
                await cmd_func(**func_kwargs)
                return
            await cmd_func()

        tindex = content.find(self.config.trigger)
        if tindex == -1:
            return
        lex = tindex+len(self.config.trigger)
        if content[lex] == self.config.lextender:
            rex = content.find(self.config.rextender, lex+1)
            word = content[lex+1: rex]
        else:
            end = content.find(' ', tindex)
            word = content[tindex+1: None if end == -1 else end]
        print("Found a trigger;", word)
        try:  # check if it's the id as keyword
            as_int = int(word)
            await self.send_childinfo(message.channel, as_int)
        except ValueError:
            await self.send_childinfo(message.channel, word)

    async def send_childinfo(self, dest, identifier):
        msg_template = "**{} - {}**[{}:star:]\nRole: {} | Element: {}\nHP: {}\nAttack: {}\nAgility: {}\nDefense: {}\nCritical: {}\n{}{}_i.png"
        c = self.json.get_child_by_identifier(identifier)
        if c is not None:
            if self.config.debug:
                return await self.send_message(dest, msg_template.format(c[JSON_NAME], c[JSON_EN_NAME], c[JSON_RARITY],
                                                                         Role(c[JSON_ROLE]).name, Element(c[JSON_ELEMENT]).name, c[JSON_STAT_HP],
                                                                         c[JSON_STAT_ATK], c[JSON_STAT_AGI],
                                                                         c[JSON_STAT_DEF], c[JSON_STAT_CRIT],
                                                                         INVEN_IMAGE_URL, c[JSON_INVEN_ID]))
            return await self.send_message(dest, c)

    async def c_create_child_entry(self, **kwargs):
        self.json.add_entry(kwargs)

    async def c_reload_json(self):
        self.json = JSONHelper("resources/children.json")

    async def c_debug(self):
        self.config.debug = not self.config.debug
        print("Debug toggled to", self.config.debug)

    async def c_logout(self):
        self.logout()