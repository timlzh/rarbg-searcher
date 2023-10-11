FROM python:3.8-slim-buster

COPY app /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]