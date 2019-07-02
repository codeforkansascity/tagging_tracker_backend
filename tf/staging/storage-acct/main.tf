provider "azurerm" {
  version = "< 2.0.0"

  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  tenant_id       = "${var.tenant_id}"
}

resource "azurerm_resource_group" "storage_acct_staging" {
  name     = "storage-staging"
  location = "${var.location}"
}

resource "azurerm_storage_account" "storage_acct_staging" {
  name                     = "taggingtrackerstaging"
  resource_group_name      = "${azurerm_resource_group.storage_acct_staging.name}"
  location                 = "${var.location}"
  account_tier             = "Standard"
  account_replication_type = "GRS"

  tags = {
    environment = "Staging"
  }
}

resource "azurerm_storage_share" "staging_share" {
  name = "staging-share"

  resource_group_name  = "${azurerm_resource_group.storage_acct_staging.name}"
  storage_account_name = "${azurerm_storage_account.storage_acct_staging.name}"

  quota = 50
}
