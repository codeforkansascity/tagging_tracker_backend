output "app_fqdn" {
  value = "${azurerm_container_group.tagging_tracker.fqdn}"
}
