resource "kubernetes_ingress" "ingress" {
  count = var.ingress_host == null ? 0 : 1

  metadata {
    name      = local.name
    namespace = kubernetes_namespace.namespace.metadata.0.name
    labels = merge({
      "app.kubernetes.io/name" : local.name
    }, var.labels)
    annotations = var.ingress_annotations
  }
  spec {
    ingress_class_name = var.ingress_class_name
    tls {
      hosts       = [var.ingress_host]
      secret_name = "${local.name}-tls"
    }
    rule {
      host = var.ingress_host
      http {
        path {
          path = "/"
        }
      }
    }
  }
}