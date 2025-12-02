terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = "${var.region}-b"
}

resource "google_sql_database" "staging_db" {
  name     = "biocirv-staging"
  instance = google_sql_database_instance.staging_db_instance.name
}

resource "google_sql_database_instance" "staging_db_instance" {
  name                = "biocirv-staging"
  database_version    = "POSTGRES_17"
  region              = var.region
  deletion_protection = true

  settings {
    tier    = "db-custom-2-8192"
    edition = "ENTERPRISE"
  }
}
