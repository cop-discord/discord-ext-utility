from discord.ext.commands.converter import MemberConverter
from fast_string_match import closest_match_distance as cmd
import re
from discord import Member
from discord.ext.commands import Context
from typing import Optional, Union
from discord.ext.commands.errors import MemberNotFound

class MemberConvert(MemberConverter):
    async def convert(self, ctx: Context, arg: Union[int, str]) -> Optional[Member]:
        _id = re.match(r'([0-9]{15,20})$', arg) or re.match(r'<@!?([0-9]{15,20})>$', arg)
        if _id is not None:
            _id = int(_id.group(1))
            if member := ctx.guild.get_member(_id):
                return member
            else: raise MemberNotFound(arg)
        names = {name: member.id for member in ctx.guild.members for name in [member.global_name, member.nick, member.display_name, member.name] if name}
        match = cmd(arg, list(names.keys()))
        if not match: 
            raise MemberNotFound(arg)
        member = ctx.guild.get_member(names[match])
        if not member:
            raise MemberNotFound(arg)


MemberConverter.convert = MemberConvert.convert
