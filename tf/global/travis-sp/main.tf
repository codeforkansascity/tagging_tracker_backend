provider "azurerm" {
  version = "=1.24.0"

  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  tenant_id       = "${var.tenant_id}"
}

resource "azurerm_resource_group" "binfra" {
  location = "${var.location}"
  name = "travis-ci"

  tags {
    Environment = "Global"
  }
}

resource "azurerm_azuread_application" "travisci" {
  name = "travisci"
}

resource "azurerm_azuread_service_principal" "travisci" {
  application_id = "${azurerm_azuread_application.travisci.application_id}"
}

resource "azurerm_azuread_service_principal_password" "travisci" {
  end_date = "2020-01-01T00:00:00Z"
  service_principal_id = "${azurerm_azuread_service_principal.travisci.id}"
  value = "${var.travisci_sp_password}"
}


resource "azurerm_role_assignment" "travisci" {
  principal_id = "${azurerm_azuread_service_principal.travisci.id}"
  scope = "${var.container_resource_group}"
  role_definition_name = "AcrPush"
}
