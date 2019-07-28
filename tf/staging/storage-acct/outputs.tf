output "storage_account_key" {
  value = "${azurerm_storage_account.storage_acct_staging.primary_access_key}"
}
output "storage_account_name" {
  value = "${azurerm_storage_account.storage_acct_staging.name}"
}
output "storage_share_name" {
  value = "${azurerm_storage_share.staging_share.name}"
}
