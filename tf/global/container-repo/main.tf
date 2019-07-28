provider "azurerm" {
  version = "< 2.0.0"

  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  tenant_id       = "${var.tenant_id}"
}

resource "azurerm_resource_group" "binfra" {
  location = "${var.location}"
  name = "${var.container_resource_group_name}"

  tags {
    Environment = "Global"
  }
}


resource "azurerm_container_registry" "acr" {
  location = "${var.location}"
  name = "${var.container_repo_name}"
  sku = "Basic"
  resource_group_name = "${azurerm_resource_group.binfra.name}"

  tags {
    Environment = "Global"
  }
}
