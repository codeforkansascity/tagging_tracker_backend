output "container_repo_url" {
  value = "${azurerm_container_registry.acr.login_server}"
}

output "resource_group_id" {
  value = "${azurerm_resource_group.binfra.id}"
}
