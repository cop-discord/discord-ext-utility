from unidecode_rs import decode
from discord import Message
import discord

class Message(Message):
    @property
    def decoded_content(self):
        return decode(self.clean_content)

discord.Message.decoded_content = Message.decoded_content
