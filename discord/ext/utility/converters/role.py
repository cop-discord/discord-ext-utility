from discord.ext.commands.converter import RoleConverter
from discord.ext.commands import Context
from discord.ext.commands.errors import RoleNotFound
from fast_string_match import closest_match
from typing import Union, Optional, List
import discord

class MultipleRoles(RoleConverter):
    async def convert(self, ctx: Context, argument: str) -> Optional[List[discord.Role]]:
        if argument.count(', ') > 0:
            arguments = argument.split(', ')
        elif argument.count(',') > 0:
            arguments = argument.split(',')
        else:
            raise ValueError('No splitting arguments like `,` or `, ` found in input')
        roles = [await Role.convert(ctx, arg) for arg in arguments]
        if len(roles) == 0: raise RoleNotFound('no roles could be found')
        return roles

class Role(RoleConverter):
    async def convert(self, ctx: Context, argument: Union[int,str]) -> Optional[discord.Role]:
        try:
            return await super().convert(ctx, argument)
        except:
            pass
        if isinstance(argument, int):
            if role := ctx.guild.get_role(argument):
                return role
            else:
                argument = str(argument)
        roles = {r.name:str(r.id) for r in ctx.guild.roles}
        if match := closest_match(argument, list(roles.keys())):
            role = ctx.guild.get_role(int(roles[match]))
        else:
            role = None
        if role == None:
            raise RoleNotFound(f"No role found under the input `{argument}`")
        return role
