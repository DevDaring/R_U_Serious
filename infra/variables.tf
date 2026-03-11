variable "do_token" {
  description = "DigitalOcean Personal Access Token"
  type        = string
  sensitive   = true
}

variable "ssh_key_id" {
  description = "Numeric ID of the SSH key uploaded to DigitalOcean"
  type        = string
}

variable "gradient_api_key" {
  description = "DigitalOcean Gradient AI API Key"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "DigitalOcean region"
  type        = string
  default     = "blr1"
}

variable "droplet_size" {
  description = "Droplet size slug"
  type        = string
  default     = "s-2vcpu-4gb"
}
