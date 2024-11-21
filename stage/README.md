# Развертывание на сервере stage-окружения

Для запуска приложения вам понадобится Docker, Docker Compose. Инструкции по его установке ищите на официальных сайтах:

- [Get Started with Docker](https://www.docker.com/get-started/)

## Переменнные окружения

Cоздайте файл `.env` в каталоге `/opt/star_burger/stage/` и присвойте значения переменным окружения в формате:
ПЕРЕМЕННАЯ=значение.

- `DEBUG` — дебаг-режим. Для dev-разработки поставьте `False`.
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на
  вашем сайте. Присвойте значение переменной `django-insecure-0if40nf4nf93n4`.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- `YANDEX_MAP_API` — API Яндекс-геокодера. Как получить токен
  смотреть [здесь](https://dvmn.org/encyclopedia/api-docs/yandex-geocoder-api/).
- `ROLLBAR_ACCESS_TOKEN` — токен доступа к проекту для мониторинга исключений в Rollbar. Создайте проект
  по [ссылке](https://rollbar.com/). Выберите свой фреймворк, чтобы начать работу с
  Rollbar SDK, и интегрируйте SDK в ваш проект по инструкции.
- `ENVIRONMENT` — название окружения или инсталляции сайта в Rollbar. Например, `stage`.
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` - пользователь, пароль и назвние БД postgres.
- `DB_URL` — однострочный адрес к базе данных Postgres в формате `postgres://USER:PASSWORD@dbT:5432/NAME`. Больше
  информации в [документации](https://github.com/jacobian/dj-database-url).

## Как запустить stage-версию сайта

Перейдите в каталог на сервере и скачайте код:

```sh
cd /opt/
git clone https://github.com/devmanorg/star-burger.git
```

Cоздайте файл `.env` в каталоге `/opt/star_burger/stage/` и присвойте значения переменным окружения в формате:
ПЕРЕМЕННАЯ=значение.

```sh
cd /opt/star_burger/stage/
touch .env
nano .env
```

Настройте Nginx на раздачу медиа-файлов и статик-файлов. Для этого в папке `/etc/nginx/sites-enabled/` создайте любой
файл без расширения (например, starburder) и скопируйте в него конфиг:

```sh
server {
    server_name starburgerrr.ru;
    location /media/ {
        alias /opt/star_burger/media/;
    }
    location /static/ {
        alias /opt/star_burger/staticfiles/;
    }
    location /bundles/ {
        alias /opt/star_burger/bundles/;
    }
    location / {
        include '/etc/nginx/proxy_params';
        proxy_pass http://127.0.0.1:8080/;
    }
}
```

Удалите дефолтный конфиг `/etc/nginx/sites-enabled/default`.

Создайте юнит `star-burger.service` в каталоге `/etc/systemd/system` следующего содержания:

```sh
[Unit]
Description=Django service
After=network.target
Requires=docker.service

[Service]
WorkingDirectory=/opt/star-burger/stage/
ExecStart=docker-compose up
Restart=always

[Install]
WantedBy=multi-user.target
```

Настройте втоматическое обновление сертификатов Certbot для Nginx
по [туториалу](https://dvmn.org/encyclopedia/deploy/renewing-certbot-certificates-for-nginx-using-a-systemd-timer/) и
запустите bash-скрипт командой:

```sh
./deploy_star_burger.sh
```

Несколько команд:

```shell
$ docker-compose exec -it {имя_контейнера} /bin/sh # зайти в контейнер
$ docker-compose exec backend python3 manage.py createsuperuser  # создаём в БД учётку суперпользователя
$ docker-compose exec backend python3 manage.py loaddata db.json # при необходимости загрузите тестовые данные в БД
$ docker ps #выводит все контейнеры
$ docker images #выводит все образы
$ docker volume ls #выводит все тома хранения данных
```

## Инструкция по быстрому обновлению кода на сервере

Подключаясь к серверу по ssh вы сначала оказываетесь в домашней директории пользователя, для быстрого
автоматического деплоя положите туда bash-скрипт. Запустите bash-скрипт командой:

```sh
./deploy_star_burger.sh
```

Готово. Пример сайта будет доступен по адресу [https://starburgerrr.ru/](https://starburgerrr.ru/).

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу
был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).
