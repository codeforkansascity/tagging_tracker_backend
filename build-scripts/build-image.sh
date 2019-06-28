#!/usr/bin/env bash

IMG_NAME="${DOCKER_REPO_URL}/tagging-tracker"

SHORT_HASH=$(git rev-parse --short HEAD)

docker build . -t $IMG_NAME
docker tag $IMG_NAME $IMG_NAME:$SHORT_HASH
echo $DOCKER_REPO_PW | \
    docker login $DOCKER_REPO_URL \
    --username $DOCKER_REPO_USER \
    --password-stdin
docker push $IMG_NAME
