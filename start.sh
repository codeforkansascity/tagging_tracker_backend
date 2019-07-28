#!/usr/bin/env bash

make rundb
export DEBUG=1

# Check if we have unapplied migrations
if python -W ignore manage.py showmigrations --plan | grep "\[ \]" -q; then
    echo "Migrations found"
    python -W ignore manage.py makemigrations
    python -W ignore manage.py migrate
    make start
else
    echo "No pending migrations"

    # Check that DB container is up and running
    if ! [ -x "$(command -v nc)" ]; then
        echo "netcat not on system."
        echo "If django server fails to connect to db press Ctrl+C and run 'make start' again"
    else
        while ! nc -z localhost 5432; do
            echo "Waiting for DB container to boot"
            sleep 0.5 # wait for half a second
        done
    fi

    # Run dev server
    python manage.py runserver
fi
