resource "kubernetes_service_account" "service_account" {
  metadata {
    name      = local.name
    namespace = kubernetes_namespace.namespace.metadata.0.name
    labels = merge({
      "app.kubernetes.io/name" : local.name
    }, var.labels)
  }
}