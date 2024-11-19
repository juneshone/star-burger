FROM python:3.10

WORKDIR /opt/star-burger
COPY requirements.txt /opt/star-burger/
RUN apt update && apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib && pip3 install --no-cache-dir -r requirements.txt
COPY . .
