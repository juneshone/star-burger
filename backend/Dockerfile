FROM python:3.10

WORKDIR /opt/star-burger
COPY requirements.txt /opt/star-burger/
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*
COPY . .
