variable "image" {
  type = string
  default = ""
}

variable "image_pull_policy" {
  type = string
  default = "Always"
}

resource "kubernetes_namespace" "namespace" {
  metadata {
    name = "pauls-land"
  }
}

resource "kubernetes_deployment" "deployment" {
  metadata {
    name = "paul"
    namespace = kubernetes_namespace.namespace.metadata.name
  }
  spec {
    template {
      metadata {}
      spec {
        container {
          name = "paul"
          image = ""
          image_pull_policy = ""
        }
      }
    }
  }
}