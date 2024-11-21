#!/bin/bash
set -e

cd /opt/star-burger/stage/

echo Обновление кода на сервере
git pull git@github.com:juneshone/star-burger.git

echo Развертывание
docker-compose -f docker-compose.yaml up --build -d

echo Пересборка статики Django
docker-compose -f docker-compose.yaml exec backend python3 manage.py collectstatic --noinput

echo Применение дата-миграций
docker-compose -f docker-compose.yaml exec backend python3 manage.py migrate

echo Перезапуск сервисов systemctl
sudo systemctl restart star-burger.service
sudo systemctl reload nginx.service

hash=$(git rev-parse --verify HEAD)
rollbar_token=$ROLLBAR_ACCESS_TOKEN
curl --request POST \
    --url https://api.rollbar.com/api/1/deploy \
    --header 'accept: application/json' \
    --header 'content-type: application/json' \
    --header 'X-Rollbar-Access-Token: '$rollbar_token'' \
    --data '{"environment": "production", "revision": "'"$hash"'", "rollbar_username": "juneshone", "local_username": "juneshone"}'
echo Успешное завершение деплоя
