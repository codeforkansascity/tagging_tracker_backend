#!/bin/bash

mkdir -p /code/logs/
touch /code/logs/gunicorn.log
touch /code/logs/access.log
touch /code/logs/error.log
tail -n 0 -f /code/logs/*.log &

python3 manage.py makemigrations
python3 manage.py migrate

echo 'Starting Gunicorn.'
exec gunicorn tagging_tracker.wsgi:application \
    --name tagging_tracker \
    --bind unix:/nginx/tagging_tracker.sock \
    --workers 3 \
    --log-level=debug \
    --log-file=/code/logs/gunicorn.log \
    --access-logfile=/code/logs/access.log \
    --reload &

echo 'Starting nginx'
exec service nginx start
