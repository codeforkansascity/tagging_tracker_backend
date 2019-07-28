variable "subscription_id" {
  type = "string"
}
variable "client_id" {
  type = "string"
}
variable "client_secret" {
  type = "string"
}
variable "tenant_id" {
  type = "string"
}
variable "location" {
  default = "Central US"
  type = "string"
}
variable "container_repo_url" {
  type = "string"
}
variable "container_repo_user" {
  type = "string"
}
variable "container_repo_password" {
  type = "string"
}
variable "storage_share_name" {
  type = "string"
}
variable "storage_account_key" {
  type = "string"
}
variable "storage_account_name" {
  type = "string"
}
