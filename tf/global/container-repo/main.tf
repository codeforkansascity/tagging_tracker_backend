provider "azurerm" {
  version = "=1.24.0"

  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  tenant_id       = "${var.tenant_id}"
}

resource "azurerm_resource_group" "binfra" {
  location = "${var.location}"
  name = "containerInfra"
}


resource "azurerm_container_registry" "acr" {
  location = "${var.location}"
  name = "wpR6r5k9hDLpK1VPEG6l"
  sku = "Basic"
  resource_group_name = "${azurerm_resource_group.binfra.name}"
}

resource "azurerm_user_assigned_identity" "travisci" {
  location = "${var.location}"
  resource_group_name = "${azurerm_resource_group.binfra.name}"
  name = "travis-ci"
}


resource "azurerm_role_assignment" "travisci" {
  principal_id = "${azurerm_user_assigned_identity.travisci.principal_id}"
  scope = "${azurerm_resource_group.binfra.id}"
  role_definition_name = "acrpush"
}
