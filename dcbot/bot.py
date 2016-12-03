from dcbot.config import Config
from dcbot.children_manager import ChildrenManager
from dcbot.permission_manager import PermissionManager
from dcbot.constants import *

from functools import wraps

import datetime
import discord
import inspect
import shlex
import sys
import traceback


class DestinyChildBot(discord.Client):
    ele_color = {Attribute.fire.value: 0xFF331C, Attribute.dark.value: 0x7C4E98, Attribute.light.value: 0xC8C270,
                 Attribute.forest.value: 0x83A04C, Attribute.water.value: 0x2691E4}

    def __init__(self, config_file='config/config.ini'):
        self.config = Config(config_file)
        self.children_mngr = ChildrenManager('resources/children.json')
        self.perm_mngr = PermissionManager()
        super().__init__()

    def superuser(func):
        @wraps(func)
        async def wrapper(self, **kwargs):
            if self.perm_mngr.is_superuser(kwargs['message'].author.id):
                return await func(self, **kwargs)
            return  # skip if not in superuser list
        return wrapper

    def get_img_url(self, child):
        if self.config.use_inven:
            return "{}{}_i.png".format(INVEN_IMAGE_URL, child[JSON_INVEN_ID])
        return "{}{}.png".format(DROPBOX_IMAGE_URL, child[JSON_EN_NAME].lower().replace('\'', '').replace(' ', '_'))

    def run(self):
        super().run(self.config.token)

    async def on_error(self, event, *args, **kwargs):
        traceback.print_exc()

    async def on_ready(self):
        print("Successfully connected!")

    async def on_message(self, message):
        print("[{}]@{}:{}".format(message.server, message.channel, message.content)
              .encode(sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding))
        if message.author == self.user:
            return

        content = message.content.strip()  # type: str

        if not content.startswith(self.config.command_trigger):
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

        children = []
        for id in activators:
            try:  # check if it's the id as keyword
                identifier = int(id)
            except ValueError:
                identifier = id
            child = self.children_mngr.get_child_by_identifier(identifier)
            if not child:
                await self.send_message(message.channel, "Didn't recognize child name/id: {}".format(id))
            else:
                children.append(child)

        command, *args = shlex.split(content[len(self.config.command_trigger):])
        i = 0
        l = len(args)
        while i < l:
            try:
                args[i] = int(args[i])
                i += 1
            except ValueError:
                if args[i][0] == self.config.activator_left and args[i][-1] == self.config.activator_right:
                    del args[i]
                    l -= 1
                else:
                    i += 1

        try:
            cmd_func = getattr(self, 'c_{}'.format(command), None)
            if not cmd_func:
                return

            parameters = inspect.signature(cmd_func).parameters.copy()

            func_kwargs = dict()
            if parameters.pop('message', None):
                func_kwargs['message'] = message
            if parameters.pop('channel', None):
                func_kwargs['channel'] = message.channel
            if parameters.pop('author', None):
                func_kwargs['author'] = message.author
            if parameters.pop('children', None):
                func_kwargs['children'] = children
            if parameters.pop('args', None):
                func_kwargs['args'] = args

            print("Calling function:", cmd_func)
            await cmd_func(**func_kwargs)
        except Exception as e:
            await self.send_message(message.channel, "```{}```".format(traceback.format_exc()))
        return

    @superuser
    async def c_debug(self, message):
        self.config.debug = not self.config.debug
        print("Debug toggled to", self.config.debug)

    @superuser
    async def c_add_superuser(self, message, args):
        self.perm_mngr.add_superuser(args[0])

    @superuser
    async def c_switch_url(self, message):
        self.config.use_inven = not self.config.use_inven
        await self.send_message(message.channel, "Using {} url for images."
                                .format("inven" if self.config.use_inven else "dropbox"))

    @superuser
    async def c_nickname(self, message, children, args): # change it so that it adds the nickname to the id rather then the english name, cause names can always change, ids do not, also check for duplicates etc
        if len(args) == 1 and len(children) == 1:
            self.children_mngr.add_nickname(children[0], args[0])
        else:
            await self.send_message(message.channel, "Couldn't add nickname to child")

    @superuser
    async def c_rnickname(self, message, args):
        if len(args) == 1:
            self.children_mngr.remove_nickname(args[0])

    @superuser
    async def c_get_nicknames(self, message, children):
        if not children:
            await self.send_message(message.channel, "```{}```".format(self.children_mngr.nicknames))
            return
        for child in children:
            await self.send_message(message.channel, "{}'s nicknames: {}".format(child[JSON_EN_NAME], self.children_mngr.get_nicknames(child)))

    @superuser
    async def c_update_json(self, message, args):
        success = self.children_mngr.update_children_by_url(args[0])
        await self.send_message(message.channel, "Update succeeded" if success else "Update failed")

    async def c_am_i_superuser(self, message):
        await self.send_message(message.channel, "->{}".format(self.perm_mngr.is_superuser(message.author.id)))

    async def c_servertime(self, message):
        utc = datetime.datetime.now(datetime.timezone.utc).time()
        utc = utc.replace(hour=(utc.hour+9)%24)
        await self.send_message(message.channel, "Current Server Time is: {}".format(utc.strftime("%H:%M:%S")))

    async def c_info(self, message, children):
        for c in children:
            emb = discord.Embed(type='rich', colour=DestinyChildBot.ele_color[c[JSON_ATTRIBUTE_ID]])
            emb.set_author(name="{} - {}[{}⭐]".format(c[JSON_NAME], c[JSON_EN_NAME], c[JSON_RARITY]))
            emb.add_field(name="Role", value=Role(c[JSON_ROLE_ID]).name.capitalize(), inline=True)
            emb.add_field(name="Attribute", value=Attribute(c[JSON_ATTRIBUTE_ID]).name.capitalize(), inline=True)
            emb.set_thumbnail(url=self.get_img_url(c))
            await self.send_message(message.channel, embed=emb)

    async def c_skills(self, message, children, args):
        for c in children:
            if args and args[0] == "korean":
                c = c.copy()
                c[JSON_SKILL1_DESC_EN] = ''
                c[JSON_SKILL1_DESC_EN] = ''
                c[JSON_SKILL1_DESC_EN] = ''
                c[JSON_SKILL1_DESC_EN] = ''
                c[JSON_SKILL1_DESC_EN] = ''
            emb = discord.Embed(type='rich', colour=DestinyChildBot.ele_color[c[JSON_ATTRIBUTE_ID]])
            emb.set_author(name="{} - {}'s skills".format(c[JSON_NAME], c[JSON_EN_NAME]))
            emb.add_field(name="Basic Attack", value=c[JSON_SKILL1_DESC_EN] or c[JSON_SKILL1_DESC], inline=False)
            emb.add_field(name="Tap", value=c[JSON_SKILL2_DESC_EN] or c[JSON_SKILL2_DESC], inline=False)
            emb.add_field(name="Slide", value=c[JSON_SKILL3_DESC_EN] or c[JSON_SKILL3_DESC], inline=False)
            emb.add_field(name="Drive", value=c[JSON_SKILL4_DESC_EN] or c[JSON_SKILL4_DESC], inline=False)
            emb.add_field(name="Leader", value=c[JSON_SKILL5_DESC_EN] or c[JSON_SKILL5_DESC], inline=False)
            emb.set_thumbnail(url=self.get_img_url(c))
            await self.send_message(message.channel, embed=emb)
