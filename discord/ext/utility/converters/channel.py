from fast_string_match import closest_match_distance as cmd
from discord import TextChannel, VoiceChannel, CategoryChannel
from discord.abc import GuildChannel
from discord.ext.commands import CommandError, GuildChannelConverter, TextChannelConverter, VoiceChannelConverter, Context, CategoryChannelConverter
from typing import Union, Optional, List
from typing_extensions import Self
from ..regex import DISCORD_ID, DISCORD_CHANNEL_MENTION


def get_match(query: str, options: List[str]) -> str:
    if match := cmd(query, options):
        return match
    else: raise CommandError(f"Channel **{query}** not found")

class TextConverter(TextChannelConverter):
    async def convert(self: Self, ctx: Context, argument: Union[int, str]) -> Optional[TextChannel]:
        if match := DISCORD_ID.match(argument):
            channel = ctx.guild.get_channel(int(match.group(1)))
        if match := DISCORD_CHANNEL_MENTION.match(argument):
            channel = ctx.guild.get_channel(int(match.group(1)))
        channels = {channel.name: channel for channel in ctx.guild.text_channels}
        match = get_match(argument, channels.keys())
        if not match:
            raise CommandError(f"Text channel **{argument}** not found")
        return channels[match]

class VoiceConverter(VoiceChannelConverter):
    async def convert(self: Self, ctx: Context, argument: Union[int, str]) -> Optional[VoiceChannel]:
        if match := DISCORD_ID.match(argument):
            channel = ctx.guild.get_channel(int(match.group(1)))
        if match := DISCORD_CHANNEL_MENTION.match(argument):
            channel = ctx.guild.get_channel(int(match.group(1)))
        channels = {channel.name: channel for channel in ctx.guild.voice_channels}
        match = get_match(argument, channels.keys())
        if not match:
            raise CommandError(f"Voice channel **{argument}** not found")
        return channels[match]

class ChannelConverter(GuildChannelConverter):
    async def convert(self: Self, ctx: Context, argument: Union[int, str]) -> Optional[GuildChannel]:
        if match := DISCORD_ID.match(argument):
            channel = ctx.guild.get_channel(int(match.group(1)))
        if match := DISCORD_CHANNEL_MENTION.match(argument):
            channel = ctx.guild.get_channel(int(match.group(1)))
        channels = {channel.name: channel for channel in ctx.guild.channels}
        match = get_match(argument, channels.keys())
        if not match:
            raise CommandError(f"Channel **{argument}** not found")
        return channels[match]
    
class CategoryConverter(CategoryChannelConverter):
    async def convert(self: Self, ctx: Context, argument: Union[int, str]) -> Optional[CategoryChannel]:
        if match := DISCORD_ID.match(argument):
            channel = ctx.guild.get_channel(int(match.group(1)))
        if match := DISCORD_CHANNEL_MENTION.match(argument):
            channel = ctx.guild.get_channel(int(match.group(1)))
        channels = {channel.name: channel for channel in ctx.guild.categories}
        match = get_match(argument, channels.keys())
        if not match:
            raise CommandError(f"Category **{argument}** not found")
        return channels[match]
    
CategoryChannelConverter.convert = CategoryConverter.convert
TextChannelConverter.convert = TextConverter.convert
VoiceChannelConverter.convert = VoiceConverter.convert
GuildChannelConverter.convert = ChannelConverter.convert


