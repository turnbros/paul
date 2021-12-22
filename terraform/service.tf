resource "kubernetes_service" "service" {
  metadata {
    name      = local.name
    namespace = kubernetes_namespace.namespace.metadata.0.name
    labels = merge({
      "app.kubernetes.io/name" : local.name
    }, var.labels)
  }
  spec {
    port {
      name        = "http"
      protocol    = "TCP"
      port        = var.bind_port
      target_port = var.bind_port
    }
    selector = {
      "app.kubernetes.io/name" : local.name
    }
  }
}