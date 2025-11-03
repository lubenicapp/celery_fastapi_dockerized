import os
import time
import json
from celery import Celery
import redis

BROKER_URL = os.getenv('BROKER_URL', 'amqp://broker:5672//')

app = Celery('events', broker=BROKER_URL)

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(redis_url)


@app.task(name='process_event')
def process_event(event, task_id):
    print(f"processing event : {event} ; task_id : {task_id}")

    # Publish the result to Redis for WebSocket notifications
    try:
        for i in range(5):
            time.sleep(1)
            r.publish(task_id, f"Processed event: {event} -  step : {i}")
    except Exception as e:
        print(f"Error publishing to Redis: {e}")

    return f"Successfully processed event: {event}"
