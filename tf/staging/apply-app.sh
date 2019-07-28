#!/usr/bin/env bash

source ../../secrets.sh

cd ./app; terraform apply -auto-approve
