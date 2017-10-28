#!/bin/bash
echo "Initializing Django server"
cd /SIEForum
echo "Installing requirements"
pip install -r requirements.txt
echo "Collecting static files"
python manage.py collectstatic -c --noinput
echo "Make migrations"
python manage.py makemigrations
echo "Migrating databases"
python manage.py migrate
echo "Compiling messages"
python manage.py compilemessages
echo "Initializing crontab"
/etc/init.d/cron start
crontab cron.txt
echo "Starting uwsgi"
uwsgi --ini /SIEForum_uwsgi.ini
