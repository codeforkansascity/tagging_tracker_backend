output "app_fqdn" {
  value = "${azurerm_container_group.tagging_tracker.fqdn}"
}
output "app_public_ip" {
  value = "${azurerm_container_group.tagging_tracker.ip_address}"
}
