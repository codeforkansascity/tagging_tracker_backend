#!/usr/bin/env bash

source ../../secrets.sh

cd ./app; terraform destroy -auto-approve
