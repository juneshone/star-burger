#!/bin/bash
set -e

cd /opt/star-burger/

echo Обновление кода на сервере
git pull git@github.com:juneshone/star-burger.git

echo Установка библиотек
source venv/bin/activate
pip3 install -r requirements.txt
npm ci --dev

echo Пересборка JS-код
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

echo Пересборка статики Django
python3 manage.py collectstatic --noinput

echo Применение дата-миграций
python3 manage.py migrate --noinput

echo Перезапуск сервисов systemctl
sudo systemctl restart star-burger.service
sudo systemctl reload nginx.service

hash=$(git rev-parse --verify HEAD)
rollbar_token=$ROLLBAR_ACCESS_TOKEN
curl --request POST \
    --url https://api.rollbar.com/api/1/deploy \
    --header 'accept: application/json' \
    --header 'content-type: application/json' \
    --header 'X-Rollbar-Access-Token: $rollbar_token' \
    --data '{"environment": "production", "revision": "'"$hash"'", "rollbar_username": "juneshone", "local_username": "juneshone"}'
echo Успешное завершение деплоя
