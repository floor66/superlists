Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.3
* Git
* Pip

eg, on Ubuntu:

	## Downloads
	sudo apt-get install nginx/git
	sudo add-apt-repository ppa:fkrull/deadsnakes
	sudo apt-get update
	sudo apt-get install python3.3
	
	## Installation
	cd /home/floris/sites/SITENAME/
	python3.3 -m venv virtualenv
	
	## ! BUGFIX necessary for it to work properly (Ubuntu 12.04.3 Server)
	vi /home/floris/sites/SITENAME/virtualenv/bin/activation
		_OLD_VIRTUAL_PATH="$PATH"
		PATH="$VIRTUAL_ENV/bin:$PATH"
		PATH="$VIRTUAL_ENV/local/bin:$PATH"  # Line addition
		export PATH
	
	source /home/floris/sites/SITENAME/virtualenv/bin/activation
	wget http://python-distribute.org/distribute_setup.py
	wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
	python distribute_setup.py
	python get-pip.py
	
	## TODO: add further configuration. This is just "basic" configuration.
	
	
## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
`--sites
   `--SITENAME
      `-- database
	  |-- source
	  |-- static
	  |-- virtualenv
	  
	  