from discord.ext.commands.converter import UserConverter
from fast_string_match import closest_match_distance as cmd
import re
from discord import Member
from discord.ext.commands import Context
from typing import Optional, Union
from discord.ext.commands.errors import UserNotFound
from ..regex import _ID_REGEX

class UserConvert(UserConverter):
    async def convert(self, ctx: Context, arg: Union[int, str]) -> Optional[Member]:
        _id = _ID_REGEX.match(arg) or re.match(r'<@!?([0-9]{15,20})>$', arg)
        if _id is not None:
            _id = int(_id.group(1))
            if member := ctx.guild.get_member(_id):
                return member
            else:
                try: return await ctx.bot.fetch_user(_id)
                except: raise UserNotFound(_id)
        names = {name: member.id for member in ctx.bot.users for name in [member.global_name, member.display_name, member.name] if name}
        match = cmd(arg, list(names.keys()))
        if not match: 
            raise UserNotFound(arg)
        member = ctx.bot.get_user(names[match])
        if not member:
            raise UserNotFound(arg)


UserConverter.convert = UserConvert.convert
