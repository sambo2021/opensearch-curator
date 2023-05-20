FROM python:slim

WORKDIR /app

COPY config /
COPY src /app

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
