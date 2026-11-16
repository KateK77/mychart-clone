#!/bin/sh
set -eu
python backend/manage.py migrate --noinput
python backend/manage.py initialize_public_demo
exec gunicorn --chdir backend careconnect.wsgi:application --bind "0.0.0.0:${PORT:-10000}" --workers 1 --threads 4 --timeout 60 --access-logfile - --error-logfile -
