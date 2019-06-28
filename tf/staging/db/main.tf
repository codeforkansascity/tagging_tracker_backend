provider "azurerm" {
  version = "=1.24.0"

  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  tenant_id       = "${var.tenant_id}"
}

resource "azurerm_resource_group" "staging-db" {
  location = "${var.location}"
  name = "stagingDBInfra"

  tags {
    Environment = "Staging"
  }
}

resource "azurerm_postgresql_server" "staging-db" {
  administrator_login = "${var.db_admin}"
  administrator_login_password = "${var.db_password}"
  location = "${var.location}"
  name = "staging-db"
  resource_group_name = "${azurerm_resource_group.staging-db.name}"
  ssl_enforcement = "Enabled"
  version = "10.7"
  sku {
    capacity = 2
    family = "Gen5"
    name = "Basic_Gen5_2"
    tier = "Basic"
  }
  storage_profile {
    storage_mb = 10000
  }

  tags {
    Environment = "Staging"
  }
}

resource "azurerm_postgresql_database" "db" {
  charset = "UTF8"
  collation = ""
  name = "staging-db"
  resource_group_name = "${azurerm_resource_group.staging-db.name}"
  server_name = ""
}