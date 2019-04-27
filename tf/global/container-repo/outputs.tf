output "container_repo_url" {
  value = "${azurerm_container_registry.acr.login_server}"
}
