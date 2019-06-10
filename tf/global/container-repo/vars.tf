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

variable "travisci_sp_password" {
  type = "string"
}