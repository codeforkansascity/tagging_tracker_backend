#!/usr/bin/env bash

if [[ -f azure-creds.auto.tfvars ]]; then
    echo "Credential file already exists"
else
    cp azure-creds.template.tfvars azure-creds.auto.tfvars
fi
