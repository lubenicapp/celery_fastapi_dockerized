import logging

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from consumer.mytasks import add

logging.basicConfig(level=logging.INFO)
app = FastAPI()


@app.get("/")
async def dummy_job(q: str = None):
    if not q:
        raise HTTPException(HTTP_400_BAD_REQUEST)
    add.delay(4, len(q))
    return q[::-1]
