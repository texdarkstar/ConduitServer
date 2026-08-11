import discord
import logging
import pathlib
from discord import app_commands, ui, Interaction, Member, Intents
from discord.ext import commands
from os import getenv
from os.path import exists
from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)
logging.basicConfig(filename=f"log.log", level=logging.INFO)


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
            for filename in list(pathlib.Path(self.env["cog_dir"]).glob('*.py')):
                cogs[str(filename.stem).lower()] = filename
            logger.info(f"Cogs found: {cogs}")
            return cogs
        except Exception as e:
            logger.error(f"Failed to collect cog {e}")


    async def setup_hook(self):
        cogs = self.get_cogs()

        for cog in cogs:
            try:
                logger.info(f"Loading cog {cog}")
                await self.load_extension(f"{self.env["cog_dir"]}.{cog}")
            except Exception as e:
                logger.error(f"Error loading {cog}: {e}")

        g = discord.Object(id=self.env['dev_discord_id'])
        self.tree.copy_global_to(guild=g)
        await self.tree.sync(guild=g)


    async def on_guild_join(self, guild):
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)



def start(env):
    bot = ConduitBot(env=env, command_prefix="|")
    bot.run(bot.env["token"])
