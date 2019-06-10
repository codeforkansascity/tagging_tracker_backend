provider "azurerm" {
  version = "=1.24.0"

  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  tenant_id       = "${var.tenant_id}"
}


resource "azurerm_resource_group" "app_infra" {
  location = "${var.location}"
  name = "applicationInfra"
}

resource "azurerm_container_group" "tagging_tracker" {
  name                = "example-continst"
  location            = "${azurerm_resource_group.app_infra.location}"
  resource_group_name = "${azurerm_resource_group.app_infra.name}"
  ip_address_type     = "public"
  dns_name_label      = "aci-label"
  os_type             = "Linux"

  container {
    name   = "tagging-tracker-backend"
    image  = "${var.container_repo_url}/tagging-tracker:latest"
    cpu    = "0.5"
    memory = "1.5"

    ports {
      port     = 8000
      protocol = "TCP"
    }
  }
}