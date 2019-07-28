output "container_repo_user" {
  value = "${azurerm_azuread_service_principal.travisci.application_id}"
}
