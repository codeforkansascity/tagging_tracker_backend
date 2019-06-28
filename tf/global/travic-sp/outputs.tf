output "travisci_app_id" {
  value = "${azurerm_azuread_service_principal.travisci.application_id}"
}
