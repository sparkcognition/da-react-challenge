#!/bin/sh

set -e

cd /usr/src/da-react-challenge/lyrics_api

echo "Running required migrations"
python manage.py migrate
echo "Migrations Complete"


echo "Starting server"
python manage.py runserver 0.0.0.0:8000