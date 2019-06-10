output "container_repo_url" {
  value = "${azurerm_container_registry.acr.login_server}"
}

output "travisci_app_id" {
  value = "${azurerm_azuread_service_principal.travisci.id}"
}
