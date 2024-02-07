import os
from celery import Celery

BROKER_URL = os.getenv('BROKER_URL')

app = Celery('mytasks', broker=BROKER_URL)

@app.task
def add(x, y):
    return x + y
