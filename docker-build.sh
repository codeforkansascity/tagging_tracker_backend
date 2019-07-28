#!/usr/bin/env bash

: '
    TODO
    This is set to ./local to build a hidden Dockerfile to prove out the Terraform
    without creating a database in Azure. It should be set to "." to build the actual app.
'
APP_DF_LOCATION=./local

source secrets.sh

docker build ${APP_DF_LOCATION} -t ${TF_VAR_container_repo_url}/tagging-tracker
docker build ./nginx -t ${TF_VAR_container_repo_url}/tagging-tracker-nginx
