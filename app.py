import logging
import uuid
import os
import asyncio
import json
import redis.asyncio as redis_async

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette.websockets import WebSocket
from fastapi.responses import HTMLResponse

from consumer.event_investigation import process_event


logging.basicConfig(level=logging.INFO)
app = FastAPI()

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis_async.from_url(redis_url)

class EventPayload(BaseModel):
    event: str


@app.post("/event")
async def monitor_event(payload: EventPayload):
    if not isinstance(payload.event, str):
        raise HTTPException(status_code=400, detail="Event must be a string")

    task_id = "toto" # uuid.uuid4().hex

    print("sending event to be processed")
    process_event.delay(payload.event, task_id)

    return {"message": "Event received", "event": payload.event, "task_id": task_id}


@app.websocket("/ws/{task_id}")
async def ws_task(websocket: WebSocket, task_id: str):
    await websocket.accept()
    pubsub = r.pubsub()
    await pubsub.subscribe(task_id)
    try:
        async for msg in pubsub.listen():
            if msg["type"] == "message":
                await websocket.send_text(msg["data"])
    finally:
        await pubsub.unsubscribe(task_id)
        await pubsub.close()
