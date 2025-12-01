variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
  default     = "biocirv-470318"
}

variable "region" {
  description = "The GCP region to deploy resources"
  type        = string
  default     = "us-west1"
}
