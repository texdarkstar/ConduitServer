import discord
from discord import Interaction, app_commands
from discord.ext import commands
import random
import bcrypt
from utils import save_token


class Token(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="token")
    @app_commands.describe(steamid="The SteamID you are attempting to link")
    async def token(self, interaction: Interaction, steamid: int):
        token = "".join([random.choice("abcdefghijklmnopqrtuvwxyz0123456789") for i in range(8)])

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(token.encode("utf-8"), salt)
        save_token(steamid, hashed)

        await interaction.response.send_message(f"Your access token for `{steamid}` is **{token}**. Do not share this.",
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(Token(bot))
