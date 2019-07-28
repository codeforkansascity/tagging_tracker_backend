#!/usr/bin/env bash

source secrets.sh

echo "Logging into ${TF_VAR_container_repo_url}"

echo ${TF_VAR_container_repo_password} | \
    docker login \
    ${TF_VAR_container_repo_url} \
    --username ${TF_VAR_container_repo_user} \
    --password-stdin
