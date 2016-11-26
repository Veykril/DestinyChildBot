from dcbot.config import Config
from dcbot.children_manager import ChildrenManager
from dcbot.permission_manager import PermissionManager
from dcbot.constants import *

from functools import wraps

import discord

import traceback


class DestinyChildBot(discord.Client):
    ele_color = {Attribute.fire.value: 0xFF331C, Attribute.dark.value: 0x7C4E98, Attribute.light.value: 0xC8C270,
                 Attribute.forest.value: 0x00FF00, Attribute.water.value: 0x2691E4}

    def __init__(self, config_file='Config/config.ini'):
        self.config = Config(config_file)
        self.children_mngr = ChildrenManager("resources/children.json")
        self.perm_mngr = PermissionManager()
        super().__init__()

    def superuser(func):
        @wraps(func)
        async def wrapper(self, **kwargs):
            if self.perm_mngr.is_superuser(kwargs['author'].id):
                return await func(self, **kwargs)
            return  # skip if not in superuser list
        return wrapper

    def run(self):
        super().run(self.config.token)

    async def on_error(self, event, *args, **kwargs):
        traceback.print_exc()

    async def on_ready(self):
        print("Successfully connected!")

    async def on_message(self, message):  # todo check for <child> in arguments of commands
        print("[{}]@{}:{}".format(message.server, message.channel, message.content))
        if message.author == self.user:
            return

        content = message.content.strip()  # type: str

        if content.startswith(self.config.command_trigger):  # command parser
            command, *args = content[len(self.config.command_trigger):].split()
            for i in range(len(args)):
                try:
                    args[i] = int(args[i])
                except ValueError:
                    pass

            try:  # TO-DO: Make the command system nicer
                cmd_func = getattr(self, 'c_{}'.format(command))

                func_kwargs = dict()
                func_kwargs['message'] = message
                func_kwargs['author'] = message.author
                func_kwargs['args'] = args

                print("Calling function:", cmd_func)
                await cmd_func(**func_kwargs)
            except AttributeError:
                pass
            except Exception as e:
                await self.send_message(message.channel, "```{}```".format(traceback.format_exc()))
            return

        left_index = 0
        activators = []
        while True:
            left_index = content.find(self.config.activator_left, left_index)
            if left_index == -1:
                break
            right_index = content.find(self.config.activator_right, left_index)
            if right_index == -1:
                break
            activators.append(content[left_index+1: right_index])
            left_index = right_index+1

        for id in activators:
            try:  # check if it's the id as keyword
                identifier = int(id)
            except ValueError:
                identifier = id
            child = self.children_mngr.get_child_by_identifier(identifier)
            if child:
                emb = discord.Embed(type='rich', colour=DestinyChildBot.ele_color[child[JSON_ATTRIBUTE_ID]])
                emb.set_author(name="{} - {}[{}⭐]".format(child[JSON_NAME], child[JSON_EN_NAME], child[JSON_RARITY]))
                emb.add_field(name="Role", value=Role(child[JSON_ROLE_ID]).name.capitalize(), inline=True)
                emb.add_field(name="Attribute", value=Attribute(child[JSON_ATTRIBUTE_ID]).name.capitalize(), inline=True)
                emb.set_thumbnail(url="{}{}_i.png".format(INVEN_IMAGE_URL, child[JSON_INVEN_ID]))
                await self.send_message(message.channel, embed=emb)

    @superuser
    async def c_debug(self, **kwargs):
        self.config.debug = not self.config.debug
        print("Debug toggled to", self.config.debug)

    @superuser
    async def c_add_superuser(self, **kwargs):
        self.perm_mngr.add_superuser(kwargs['args'][0])

    @superuser
    async def c_nickname(self, **kwargs):
        args = kwargs['args']
        if len(args) == 2:
            self.children_mngr.add_nickname(args[0], args[1])
        else:
            await self.send_message(kwargs['channel'], "Couldn't add nickname to child")

    async def c_info(self, **kwargs):
        c = self.children_mngr.get_child_by_identifier(kwargs['args'][0])
        if c is not None:
            emb = discord.Embed(type='rich', colour=DestinyChildBot.ele_color[c[JSON_ATTRIBUTE_ID]])
            emb.set_author(name="{} - {}[{}⭐]".format(c[JSON_NAME], c[JSON_EN_NAME], c[JSON_RARITY]))
            emb.description = "Role: {} | Element: {}".format(Role(c[JSON_ROLE_ID]).name.capitalize(),
                                                              Attribute(c[JSON_ATTRIBUTE_ID]).name.capitalize())
            emb.add_field(name='HP', value=c[JSON_STAT_HP], inline=False)
            emb.add_field(name='Attack', value=c[JSON_STAT_ATK], inline=False)
            emb.add_field(name='Agility', value=c[JSON_STAT_AGI], inline=False)
            emb.add_field(name='Defense', value=c[JSON_STAT_DEF], inline=False)
            emb.add_field(name='Critical', value=c[JSON_STAT_CRIT], inline=False)
            emb.set_thumbnail(url="{}{}_i.png".format(INVEN_IMAGE_URL, c[JSON_INVEN_ID]))
            await self.send_message(kwargs['message'].channel, embed=emb)
        else:
            await self.send_message(kwargs['message'].channel, "Didn't recognize child name: {}".format(kwargs['args'][0]))

    async def c_skills(self, **kwargs):
        c = self.children_mngr.get_child_by_identifier(kwargs['args'][0])
        if c is not None:
            emb = discord.Embed(type='rich', colour=DestinyChildBot.ele_color[c[JSON_ATTRIBUTE_ID]])
            emb.set_author(name="{} - {}'s skills".format(c[JSON_NAME], c[JSON_EN_NAME]))
            emb.add_field(name="Basic Attack", value=c[JSON_SKILL1_DESC_EN] or c[JSON_SKILL1_DESC], inline=False)
            emb.add_field(name="Tap", value=c[JSON_SKILL2_DESC_EN] or c[JSON_SKILL2_DESC], inline=False)
            emb.add_field(name="Slide", value=c[JSON_SKILL3_DESC_EN] or c[JSON_SKILL3_DESC], inline=False)
            emb.add_field(name="Drive", value=c[JSON_SKILL4_DESC_EN] or c[JSON_SKILL4_DESC], inline=False)
            emb.add_field(name="Leader", value=c[JSON_SKILL5_DESC_EN] or c[JSON_SKILL5_DESC], inline=False)
            emb.set_thumbnail(url="{}{}_i.png".format(INVEN_IMAGE_URL, c[JSON_INVEN_ID]))
            await self.send_message(kwargs['message'].channel, embed=emb)
