from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
from fabric.context_managers import settings

from os import path

import random

REPO_URL = 'https://github.com/floor66/superlists.git'
SITES_FOLDER = '/home/ubuntu/sites'

env.hosts = ['floor66.no-ip.biz']
env.user = 'ubuntu'
env.key_filename = 'C:\\tddaws.pem'

def deploy():
	_create_directory_structure_if_necessary(env.host)
	source_folder = path.join(SITES_FOLDER, env.host, 'source').replace('\\', '/')
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_update_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)
	_configure_nginx(source_folder)
	_configure_upstart(source_folder)
	_start_server()

def _create_directory_structure_if_necessary(site_name):
	base_folder = path.join(SITES_FOLDER, site_name).replace('\\', '/')
	
	run('mkdir -p %s' % (base_folder,))
	
	for subfolder in ('database', 'static', 'source', 'virtualenv',):
		run('mkdir -p %s/%s' % (base_folder, subfolder,))
		
def _get_latest_source(source_folder):
	if exists(path.join(source_folder, '.git').replace('\\', '/')):
		run('cd %s && git fetch' % (source_folder,))
	else:
		run('git clone %s %s' % (REPO_URL, source_folder,))
	
	current_commit = local('git log -n 1 --format=%H', capture=True)
	run('cd %s && git reset --hard %s' % (source_folder, current_commit,))
	
def _update_settings(source_folder, site_name):
	settings_path = path.join(source_folder, 'superlists/settings.py').replace('\\', '/')
	sed(settings_path, 'DEBUG = True', 'DEBUG = False')
	append(settings_path, 'ALLOWED_HOSTS = [\'%s\']' % (site_name,))
	
	secret_key_file = path.join(source_folder, 'superlists/secret_key.py').replace('\\', '/')
	if not exists(secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''. join(random.SystemRandom().choice(chars) for _ in range(50)) 
		append(secret_key_file, 'SECRET_KEY = \'%s\'' % (key,))
	append(settings_path, 'from .secret_key import SECRET_KEY')
	
def _update_virtualenv(source_folder):
	virtualenv_folder = path.join(source_folder, '../virtualenv').replace('\\', '/')
	if not exists(path.join(virtualenv_folder, 'bin', 'pip').replace('\\', '/')):
		run('virtualenv --python=python3 %s' % (virtualenv_folder,))
	run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder,))
	
def _update_static_files(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (source_folder,))
	
def _update_database(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py syncdb --noinput' % (source_folder,))

	run('cd %s && ../virtualenv/bin/python3 manage.py syncdb --migrate --noinput' % (source_folder,))
	
def _configure_nginx(source_folder):
	nginx_conf_file = '/etc/nginx/sites-available/%s' % (env.host,)
	if not exists(nginx_conf_file):
		run('sudo sed "s/SITENAME/%s/g" %s/deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/%s' % (env.host, source_folder, env.host,))
	
	nginx_conf_file = '/etc/nginx/sites-enabled/%s' % (env.host,)
	if not exists(nginx_conf_file):
		run('sudo ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/%s' % (env.host, env.host,))
	
def _configure_upstart(source_folder):
	upstart_conf_file = '/etc/init/gunicorn-%s' % (env.host,)
	if not exists(upstart_conf_file):
		run('sudo sed "s/SITENAME/%s/g" %s/deploy_tools/gunicorn-upstart.template.conf | sudo tee /etc/init/gunicorn-%s.conf' % (env.host, source_folder, env.host,))
	
def _start_server():
	run('sudo service nginx reload')
	with settings(warn_only=True):
		run('sudo restart gunicorn-%s' % (env.host,)) # May fail if already running, so only warn
	