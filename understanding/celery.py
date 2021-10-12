import os
from decouple import config
from celery import Celery

app = Celery(
    "understanding", broker=config("BROKER_URL"), include=["understanding.tasks"]
)

if __name__ == "__main__":
    app.start()
