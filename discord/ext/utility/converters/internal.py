import re
import emoji
import aiohttp
from fast_string_match import closest_match
from discord.ext.commands import (
    Converter,
    BadArgument,
    errors,
    CommandNotFound,
    Context
)
from typing import Any, Optional
from itertools import chain
from pydantic import BaseModel

class AliasError(errors.CommandError):
    def __init__(self, message, **kwargs):
        self.message = message
        super().__init__(self.message, **kwargs)

    @property
    def message(self) -> Optional[Any]:
        return self.message

class CommandMatchError(errors.CommandError):
    def __init__(self, message, **kwargs):
        self.message = message
        super().__init__(self.message,**kwargs)

    @property
    def message(self) -> Optional[Any]:
        return self.message

class Command(Converter):
    async def convert(self, ctx: Context, argument: str):
        if command := ctx.bot.get_command(argument):
            if command.qualified_name.lower() not in ctx.bot.non_editted:
                return command
        commands = [command.qualified_name for command in ctx.bot.walk_commands()]
        if match := closest_match(argument, commands):
            if command := ctx.bot.get_command(match):
                return command
        raise CommandNotFound(f"No command could be found named `{argument}`")

class Alias(Converter):
    async def convert(self, ctx: Context, argument: str):
        if " , " in argument:
            command, alias = argument.split(' , ')
        if "," in argument:
            command, alias = argument.split(',')
        if alias.startswith(' '):
            alias = alias.lstrip()
        else:
            raise AliasError(f"please split the **command** and **alias** with a comma")
        blacklist = list(chain.from_iterable([[c.qualified_name,c.aliases] for c in ctx.bot.walk_commands()]))
        if alias in blacklist:
            raise AliasError(f"alias is already an existing command's alias")
        if _command := ctx.bot.get_command(command):
            return (_command, alias)
        else:
            _command = await Command().convert(ctx, command)
            return (_command, alias)

class ColorSchema(BaseModel):
    """
    Schema for colors
    """

    hex: str
    value: int


class AnyEmoji(Converter):
    async def convert(self, ctx: Context, argument: str):
        if emoji.is_emoji(argument):
            return argument

        emojis = re.findall(
            r"<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>",
            argument,
        )

        if len(emojis) == 0:
            raise BadArgument(f"**{argument}** is **not** an emoji")

        emoj = emojis[0]
        format = ".gif" if emoj[0] == "a" else ".png"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://cdn.discordapp.com/emojis/{emoj[2]}{format}"
            ) as response:
                return await response.read()


class EligibleVolume(Converter):
    async def convert(self, ctx: Context, argument: str):
        try:
            volume = int(argument)
        except ValueError:
            raise BadArgument("This is **not** a number")

        if volume < 0 or volume > 500:
            raise BadArgument("Volume has to be between **0** and **500**")

        return volume


class ChannelType(Converter):
    async def convert(self, ctx: Context, argument: str):
        if not argument in ["voice", "stage", "text", "category"]:
            raise BadArgument(f"**{argument}** is not a **valid** channel type")

        return argument