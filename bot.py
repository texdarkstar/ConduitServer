from logging.handlers import TimedRotatingFileHandler

import discord
import logging
import pathlib
import datetime as dt
from discord import app_commands, ui, Interaction, Member, Intents
from discord.ext import commands
from os import getenv
from os.path import exists

import checks
from env import env


if not exists(env["log_dir"]):
    mkdir(env["log_dir"])
if not exists(env["cog_dir"]):
    mkdir(env["cog_dir"])


# // logger setup //

def log_namer(default_name):
    now = dt.datetime.now()
    base, extra = default_name.split(".")
    return f"{base}.{now.year}-{now.month}-{now.day}.log"


now = dt.datetime.now()

logger = logging.getLogger()

handler = TimedRotatingFileHandler(
    f"logs/clearance_log.{now.year}-{now.month}-{now.day}.log",
    when="midnight", backupCount=7, interval=1, encoding="utf-8")

handler.namer = log_namer
fileFormatter = logging.Formatter(
    "[%(asctime)s.%(msecs)d]:[%(levelname)s] - (%(filename)s:%(funcName)s:%(lineno)d) : %(message)s",
    "%Y-%m-%d %H:%M:%S")

handler.setFormatter(fileFormatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class ConduitBot(commands.Bot):
    def __init__(self, env, intents=Intents.all(), *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.env = env
        intents.message_content = True
        intents.members = True
        intents.guilds = True


    def get_cogs(self):
        logger.info("Collecting cogs...")
        cogs = {}

        try:
            for filename in list(pathlib.Path(self.env["cog_dir"]).glob("*.py")):
                cogs[str(filename.stem).lower()] = filename
            logger.info(f"Cogs found: {[i for i in cogs.keys()]}")
            return cogs
        except Exception as e:
            logger.error(f"Failed to collect cogs\n{"*" * 8}\n{e}")


    async def setup_hook(self):
        g = discord.Object(id=self.env["dev_discord_id"])
        await self.load_cogs()
        await self.sync_commands(g)


    async def sync_commands(self, g):
        self.tree.copy_global_to(guild=g)
        await self.tree.sync(guild=g)


    async def load_cogs(self):
        cogs = self.get_cogs()

        for cog in cogs:
            try:
                logger.info(f"Loading cog {cog}")
                await self.load_extension(f"{self.env["cog_dir"]}.{cog}")
            except Exception as e:
                logger.error(f"Error loading {cog}: {e}")


    async def on_guild_join(self, guild):
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)



def start(env):
    bot = ConduitBot(env=env, command_prefix="|")

    @bot.tree.command(name="reload", description="Reload cogs")
    @app_commands.describe(sync="Global command tree resync")
    @app_commands.check(checks.is_dev_channel)
    async def reload(interaction: Interaction, sync: bool = False):
        logger.info("Reloading cogs...")
        await interaction.response.defer(ephemeral=True)

        extensions = []
        for i in bot.extensions:
            extensions.append(i)

            for cog in extensions:
                await bot.unload_extension(cog)
                logger.info(f"{cog} unloaded")

            await bot.load_cogs()

            if sync:
                for guild in bot.guilds:
                    await bot.sync_commands(guild)

            await interaction.followup.send("Reloaded cogs")


    @reload.error
    async def reload_error(interaction: Interaction, error:app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You do not have permission to use that here", ephemeral=True)

    bot.run(bot.env["token"])
