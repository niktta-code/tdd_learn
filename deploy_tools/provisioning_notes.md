Обеспечение работы нового сайта
================================
 ## Необходимые пакеты:
 * nginx
 * Python3.6+
 * virtualenv + pip
 * Git
 * pip install wheel
 
 
 например в Ubuntu
 
`sudo apt install nginx git python3-venv python3-dev gcc libpq-dev`

## Конфигурация виртуального узла Nginx
* см. nginx.template.conf
* заменить SITENAME, например, на stagin.my-domain.com

## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на stagin.my-domain.com

## Структура папок
```
/home/username
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv
```
