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
	
	## TODO: add getting pip
	
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
	  
	  