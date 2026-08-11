import json
import bot
import logging
from flask import Flask, request, jsonify
from time import time
from threading import Thread
from os import getenv
from dotenv import load_dotenv, find_dotenv

import utils

load_dotenv(find_dotenv("secret.env"))

env = {
    "port": getenv("PORT"),
    "token": getenv("TOKEN"),
    "cog_dir": getenv("COG_DIR"),
    "dev_discord_id": getenv("DEV_DISCORD_ID"),
    "owner_id": getenv("OWNER_ID")
}

logger = logging.getLogger(__name__)

flask = Flask(__name__)



@flask.route('/', methods=["POST"])
def ingest():
    if utils.authenticate(request):
        utils.ingest(json.loads(request.get_data().strip()))

    return jsonify(statusCode=200)



if __name__ == "__main__":
    bot_thread = Thread(target=bot.start, args=(env,), daemon=True)
    bot_thread.start()
    flask.run(debug=False, port=env['port'])

