from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv("secret.env"))

env = {
    "token": getenv("TOKEN"),
    "cog_dir": getenv("COG_DIR"),
    "log_dir": getenv("LOG_DIR"),
    "dev_discord_id": int(getenv("DEV_DISCORD_ID")),
    "superuser_id": int(getenv("SUPERUSER_ID")),
    "host": getenv("HOST"),
    "port": int(getenv("PORT"))
}

