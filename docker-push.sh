#!/usr/bin/env bash

source secrets.sh

docker push ${TF_VAR_container_repo_name}/tagging-tracker
docker push ${TF_VAR_container_repo_name}/tagging-tracker-nginx
