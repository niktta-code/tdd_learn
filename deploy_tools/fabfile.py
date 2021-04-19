from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random


REPO_URL = 'https://github.com/niktta-code/tdd_learn.git'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def config_server():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'

    _config_nginx(source_folder, env.host)
    _systemd_config(source_folder, env.host)
    _run_services(env.host)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')

    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    setting_path = source_folder + '/superlists/settings.py'
    sed(setting_path, "DEBUG = True", "DEBUG = False")
    sed(setting_path,
        'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
        )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(setting_path, '\nfrom .secret_key import  SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')


def _config_nginx(source_folder, site_name):
    run(f'sed "s/SITENAME/{site_name}/g" {source_folder}/deploy_tools/nginx.template.conf '
        f'| sudo tee /etc/nginx/sites-available/{site_name}')
    run(f'sudo ln -s ../sites-available/{site_name} /etc/nginx/sites-enabled/{site_name}')


def _systemd_config(source_folder, site_name):
    run(f'sed "s/SITENAME/{site_name}/g" {source_folder}/deploy_tools/gunicorn-systemd.template.service '
        f'| sudo tee /etc/systemd/system/gunicorn-{site_name}.service')


def _run_services(site_name):
    run('sudo systemctl daemon-reload')
    run('sudo systemctl reload nginx')
    run(f'sudo systemctl enable gunicorn-{site_name}')
    run(f'sudo systemctl restart gunicorn-{site_name}')
