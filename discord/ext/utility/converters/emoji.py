from discord.ext import commands
from discord.ext.commands import Context
from typing import Optional, Union, List, Any
import unicodedata, discord, re
from ..regex import DISCORD_ID, EMOJI_REGEX, DEFAULT_EMOJIS
from discord.ext.commands.converter import PartialEmojiConverter
from typing_extensions import Self

class Emoji(commands.EmojiConverter):
    async def convert(
        self: Self, ctx: "Context", argument: str
    ) -> Optional[Union[discord.Emoji, discord.PartialEmoji]]:
        result = None
        match = DISCORD_ID.match(argument) or re.match(r'<a?:[a-zA-Z0-9\_]{1,32}:([0-9]{15,20})>$', argument)
        if not match:
            result = discord.utils.get(ctx.guild.emojis, name = argument)
            if result is None:
                result = discord.utils.get(ctx.bot.emojis, name = argument)
        else:
            if emoji := ctx.bot.get_emoji(match.group(1)):
                return emoji
        if result != None:
            return result
        else:
            try:
                return unicodedata.name(argument)
            except Exception:
                try:
                    return unicodedata.name(argument[0])
                except:
                    pass

        raise commands.EmojiNotFound(argument)
    
class Emojis(commands.Converter):
    async def convert(self: Self, ctx: Context, argument: str) -> Optional[List[Any]]:
        emojis = []
        matches = EMOJI_REGEX.finditer(argument)
        for emoji in matches:
            e = emoji.groupdict()
            emojis.append(await PartialEmojiConverter().convert(ctx,f"<{e['animated']}:{e['name']}:{e['id']}>"))
        defaults = DEFAULT_EMOJIS.findall(argument)
        if len(defaults) > 0: emojis.extend(defaults)
        return emojis