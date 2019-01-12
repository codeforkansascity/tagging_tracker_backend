#!/usr/bin/env bash

# Loads local.env into environment

if [ ! -f local.env ]; then
    echo "local.env not found"
    exit 1
fi

export $(cat local.env | xargs)
