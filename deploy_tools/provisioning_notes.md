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
* sudo ln -s ../sites-available/superlists-staging.banan.cyou /etc/nginx/sites-enabled/superlists-staging.banan.cyou
* sudo systemctl reload nginx
* sudo nginx -t

## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на stagin.my-domain.com
* sudo systemctl daemon-reload
* sudo systemctl enable gunicorn-SITENAME
* sudo systemctl (re)start gunicorn-SITENAME

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


## fab deploy

fab deploy:host=nikita@superlists.banan.cyou


## fab config erver

fab config_server:host=nikita@superlists.banan.cyou