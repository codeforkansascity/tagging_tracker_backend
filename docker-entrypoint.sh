#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate

mkdir -p /code/logs/
touch /code/logs/gunicorn.log
touch /code/logs/access.log
tail -n 0 -f /code/logs/*.log &

echo 'Starting Gunicorn.'
exec gunicorn tagging_tracker.wsgi:application \
    --name tagging_tracker \
    --bind unix:/nginx/tagging_tracker.sock \
    --workers 3 \
    --log-level=info \
    --log-file=/code/logs/gunicorn.log \
    --access-logfile=/code/logs/access.log &

echo 'Starting nginx'
exec service nginx start
