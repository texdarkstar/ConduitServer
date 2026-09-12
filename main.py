import json
from pydantic import BaseModel

import bot
import logging
from datetime import datetime
from threading import Thread

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from env import *
from schema import TelemetryData
import utils



logger = logging.getLogger(__name__)

app = FastAPI()

security_bearer = HTTPBearer()


@app.post("/")
def ingest(data: TelemetryData, credentials: HTTPAuthorizationCredentials = Depends(security_bearer)):
    token = credentials.credentials
    if not utils.authenticate(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to authenticate token"
        )
    utils.ingest(data)


if __name__ == "__main__":
    bot_thread = Thread(target=bot.start, args=(env,), daemon=True)
    bot_thread.start()
    uvicorn.run("main:app", host=env["host"], port=env["port"], reload=True)

