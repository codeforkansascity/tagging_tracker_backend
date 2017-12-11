#!/bin/bash

python3 manage.py migrate

touch /code/logs/gunicorn.log
touch /code/logs/access.log
tail -n 0 -f /code/logs/*.log &
echo 'Starting nginx'
# Start Gunicorn processes
echo 'Starting Gunicorn.'
exec gunicorn tagging_tracker.wsgi:application \
    --name tagging_tracker \
    --bind unix:tagging_tracker.sock \
    --workers 3 \
    --log-level=info \
    --log-file=/code/logs/gunicorn.log \
    --access-logfile=/code/logs/access.log & 
exec service nginx start
