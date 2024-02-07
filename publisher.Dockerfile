FROM python:3.12-slim
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./consumer ./consumer
COPY ./app.py  ./app.py
