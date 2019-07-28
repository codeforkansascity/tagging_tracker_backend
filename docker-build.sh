#!/usr/bin/env bash

APP_DF_LOCATION=./local

source secrets.sh

docker build ${APP_DF_LOCATION} -t ${TF_VAR_container_repo_url}/tagging-tracker
docker build ./nginx -t ${TF_VAR_container_repo_url}/tagging-tracker-nginx
