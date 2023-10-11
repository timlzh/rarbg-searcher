FROM python:3.8-slim-buster

COPY app/requirements.txt /tmp/requirements.txt 
RUN pip install -r /tmp/requirements.txt

COPY app /app
WORKDIR /app

CMD ["python", "main.py"]
