variable "db_host" {
    type    = string
    default = getenv("DB_HOST")
}
variable "db_port" {
    type    = string
    default = getenv("DB_PORT")
}
variable "db_user" {
    type    = string
    default = getenv("DB_USER")
}
variable "db_password" {
    type    = string
    default = getenv("DB_PASSWORD")
}
variable "db_name" {
    type    = string
    default = getenv("DB_NAME")
}

locals {
    uri = "postgres://${var.db_user}:${var.db_password}@${var.db_host}:${var.db_port}/${var.db_name}?sslmode=disable"
    dev_uri = "postgres://${var.db_user}:${var.db_password}@${var.db_host}:${var.db_port}/atlas_dev_db?sslmode=disable"
}

env "local" {
  src = "file://app/db/schema/schema.sql"
  url = local.uri
  dev = local.dev_uri
}
