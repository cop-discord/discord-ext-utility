# GENERAL SETUP

"""from discord.ext.utility import apply
apply()

rest of your bot code down below"""


# Color Converting with Names
"""from discord.ext.utility import NamedColorConverter
@commands.command(name = "colorme")
async def colorme(ctx: commands.Context, color: NamedColorConverter):
    role = await ctx.guild.create_role(name = color.name, color = discord.Color.from_str(color.hex))
    await ctx.author.add_roles(role, reason = "colorme")
    return await ctx.send("successfully gave you the color **{color.name}({color.hex})**")"""


# Decoded Content
"""
async def on_message(self, message: discord.Message):
    return message.decoded_content
"""

"""WARNING Rust Cargo is required for this package. Without it, it will not function"""