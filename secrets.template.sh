#!/usr/bin/env bash

: '
    This script cannot be in the repo as it would expose credentials.
    Long term build process scripts cannot be reliant on it and instead those
    variables should be stored in the build process envars.
'

export TF_VAR_subscription_id=
export TF_VAR_client_id=
export TF_VAR_tenant_id=
export TF_VAR_client_secret=

export TF_VAR_container_resource_group_name=
export TF_VAR_container_repo_name=
export TF_VAR_container_repo_url=${TF_VAR_container_repo_name}.azurecr.io
export TF_VAR_container_resource_group=/subscriptions/${TF_VAR_subscription_id}/resourceGroups/${TF_VAR_container_resource_group_name}

export TF_VAR_container_repo_password=
# Generated
export TF_VAR_container_repo_user=

# Generated
export TF_VAR_storage_account_key=

export TF_VAR_storage_account_name=
export TF_VAR_storage_share_name=
