### Important Paul Settings ###
variable "bind_ip" {
  type = string
  description = "Which IP will Paul be listening on?"
  default = "0.0.0.0"
}
variable "bind_port" {
  type = number
  description = "Which port will Paul be listening on?"
  default = 8443
}
variable "debug_enabled" {
  type = bool
  description = "Should Paul smile less and talk more?"
  default = false
}

### Ingress Settings for Paul ###
variable "ingress_host" {
  type = string
  description = "What hostname will we reach Paul at?"
  default = null
}
variable "ingress_class_name" {
  type = string
  description = "What's the name of Pauls' ingress class?"
  default = null
}
variable "ingress_annotations" {
  type = map(string)
  description = "What annotations would you like to add to Pauls ingress?"
  default = {}
}

## Discord Connectivity Settings ###
variable "discord_client_id" {
  type = string
  description = ""
}
variable "discord_client_secret" {
  type = string
  description = ""
}

## Kubernetes Connectivity Settings ###
variable "kubernetes_endpoint" {
  type = string
  description = "Which Kubernetes cluster should Paul watch?"
  default = "https://kubernetes.default.svc"
}

### Other Boring Kubernetes Settings ###
variable "image" {
  type = string
  description = "Where do we store our Paul image?"
  default = "ghcr.io/turnbros/paul/paul:latest"
}
variable "image_pull_policy" {
  type = string
  description = "When should we pull new versions of Paul?"
  default = "Always"
}
variable "replica_count" {
  type = number
  description = "How many Pauls?"
  default = 1
}
variable "cpu_request" {
  type = string
  description = "How fast do we expect Paul to think?"
  default = "250m"
}
variable "memory_request" {
  type = string
  description = "How much do we expect Paul to remember?"
  default = "64Mi"
}
variable "cpu_limit" {
  type = string
  description = "How fast should we allow Paul to think?"
  default = "500m"
}
variable "memory_limit" {
  type = string
  description = "How much should we allow Paul to remember?"
  default = "128Mi"
}
variable "labels" {
  type = map(string)
  description = "Are there any tags we should add to the bits and pieces that make up Paul?"
  default = {}
}