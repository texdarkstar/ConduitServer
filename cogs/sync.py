import discord
from discord import Interaction, app_commands
from discord.ext import commands
import random



class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="sync")
    async def sync(self, interaction: Interaction):
        print(self.bot.env["owner_id"])
        if str(interaction.user.id) != str(self.bot.env["owner_id"]):
            await interaction.response.send_message("You are not allowed to run that command", ephemeral=True)
            return
        guilds = self.bot.guilds
        for g in guilds:
            self.bot.tree.copy_global_to(guild=g)

        await self.bot.tree.sync()
        await interaction.response.send_message("Commands synced", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Sync(bot))
