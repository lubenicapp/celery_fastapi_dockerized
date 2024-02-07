FROM python:3.12-slim
ENTRYPOINT ["celery", "-A", "consumer.mytasks", "worker"]
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./consumer  ./consumer
