#!/usr/bin/env bash

source secrets.sh

docker push ${TF_VAR_container_repo_url}/tagging-tracker
docker push ${TF_VAR_container_repo_url}/tagging-tracker-nginx
