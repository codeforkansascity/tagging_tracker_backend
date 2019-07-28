#!/usr/bin/env bash

#!/usr/bin/env bash

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
