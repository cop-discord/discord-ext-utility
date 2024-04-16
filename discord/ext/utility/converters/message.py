from discord.ext import commands
from discord.ext.commands import Context
from aiohttp import ClientSession as Session
from typing import Optional, Union
from ..regex import link
from contextlib import suppress


class Image(commands.Converter):
    async def convert(self, ctx: Context, argument: str = None) -> Optional[bytes]:
        if argument is None:
            if len(ctx.message.attachments) == 0:
                raise commands.BadArgument("No image was provided.")
            else:
                return await ctx.message.attachments[0].read()
        else:
            if "discord.com" in argument or "discordapp.com" in argument:
                async with Session() as session:
                    async with session.request("GET", f"{argument}") as response:
                        data = await response.read()
            else:
                async with Session() as session:
                    async with session.request(
                        "GET", f"https://proxy.rival.rocks?url={argument}"
                    ) as response:
                        data = await response.read()
            if not data:
                raise commands.BadArgument("No image was provided.")
            return data


class VoiceMessage(commands.Converter):
    async def convert(
        self, ctx: "Context", argument: str = None, fail: bool = True
    ) -> Optional[str]:
        """
        Convert the given argument to a link if it matches the link pattern.

        Parameters:
            ctx (Context): The context object representing the current execution context.
            argument (str): The argument to be converted.
            fail (bool, optional): Whether to raise an exception if the conversion fails. Defaults to True.

        Returns:
            Optional[str]: The converted link if the argument matches the link pattern, None otherwise.

        Raises:
            AssertionError: If fail is True and no link is found.
        """

        if match := link.match(argument):
            return match.group()

        if fail is True:
            with suppress(Exception):
                await ctx.send_help(ctx.command.qualified_name)

            assert False

    @staticmethod
    async def search(ctx: "Context", fail: bool = True) -> Optional[str]:
        """
        Retrieves the URL of the first attachment in the last 50 messages in the given context's channel.

        Parameters:
            ctx (Context): The context object representing the current execution context.
            fail (bool, optional): Specifies whether an error should be raised if no attachment is found. Defaults to True.

        Returns:
            Optional[str]: The URL of the first attachment found, or None if no attachment is found.

        Raises:
            AssertionError: If fail is True and no link is found.
        """

        async for message in ctx.channel.history(limit=50):
            if message.attachments:
                return message.attachments[0].url

        if fail is True:
            with suppress(Exception):
                await ctx.send_help(ctx.command.qualified_name)

            assert False


class Stickers(commands.Converter):
    async def convert(
        self, ctx: "Context", argument: str, fail: bool = True
    ) -> Optional[str]:
        """
        Convert the given argument to a link if it matches the link pattern.

        Parameters:
            ctx (Context): The context object representing the current execution context.
            argument (str): The argument to be converted.
            fail (bool, optional): Whether to raise an exception if the conversion fails. Defaults to True.

        Returns:
            Optional[str]: The converted link if the argument matches the link pattern, None otherwise.

        Raises:
            AssertionError: If fail is True and no link is found.
        """

        if match := link.match(argument):
            return match.group()

        if fail is True:
            with suppress(Exception):
                await ctx.send_help(ctx.command.qualified_name)

            assert False

    @staticmethod
    async def search(ctx: "Context", fail: bool = True) -> Optional[str]:
        """
        Retrieves the URL of the first attachment in the last 50 messages in the given context's channel.

        Parameters:
            ctx (Context): The context object representing the current execution context.
            fail (bool, optional): Specifies whether an error should be raised if no attachment is found. Defaults to True.

        Returns:
            Optional[str]: The URL of the first attachment found, or None if no attachment is found.

        Raises:
            AssertionError: If fail is True and no link is found.
        """
        if ctx.message.reference:
            return ctx.message.reference.resolved.stickers[0].url
        async for message in ctx.channel.history(limit=50):
            if message.stickers:
                return message.stickers[0].url

        if fail is True:
            with suppress(Exception):
                await ctx.send_help(ctx.command.qualified_name)

            assert False


class Attachment(commands.Converter):
    async def convert(
        self, ctx: "Context", argument: str, fail: bool = True
    ) -> Optional[str]:
        """
        Convert the given argument to a link if it matches the link pattern.

        Parameters:
            ctx (Context): The context object representing the current execution context.
            argument (str): The argument to be converted.
            fail (bool, optional): Whether to raise an exception if the conversion fails. Defaults to True.

        Returns:
            Optional[str]: The converted link if the argument matches the link pattern, None otherwise.

        Raises:
            AssertionError: If fail is True and no link is found.
        """

        if match := link.match(argument):
            return match.group()

        if fail is True:
            with suppress(Exception):
                await ctx.send_help(ctx.command.qualified_name)

            assert False

    @staticmethod
    async def search(ctx: "Context", fail: bool = True) -> Optional[str]:
        """
        Retrieves the URL of the first attachment in the last 50 messages in the given context's channel.

        Parameters:
            ctx (Context): The context object representing the current execution context.
            fail (bool, optional): Specifies whether an error should be raised if no attachment is found. Defaults to True.

        Returns:
            Optional[str]: The URL of the first attachment found, or None if no attachment is found.

        Raises:
            AssertionError: If fail is True and no link is found.
        """
        async for message in ctx.channel.history(limit=50):
            if message.attachments:
                return await message.attachments[0].read()

        if fail is True:
            with suppress(Exception):
                await ctx.send_help(ctx.command.qualified_name)

            assert False


class Message(commands.MessageConverter):
    async def convert(self, ctx: Context, argument: Optional[Union[int,str]] = None):
        if not argument:
            if not ctx.message.reference:
                raise commands.BadArgument("No **message** was provided.")
            else:
                return await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if isinstance(argument, int):
            return await ctx.channel.fetch_message(argument)

        if "discord.com/channels/" in argument:
            arguments = argument.split("/channels/")
            guild_id, channel_id, message_id = arguments[1].split("/")
            if guild := ctx.bot.get_guild(guild_id):
                if channel := guild.get_channel(channel_id):
                    return await channel.fetch_message(message_id)
        else:
            return await ctx.channel.fetch_message(argument)