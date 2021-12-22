resource "kubernetes_role" "role" {
  metadata {
    name      = local.name
    namespace = kubernetes_namespace.namespace.metadata.0.name
    labels = merge({
      "app.kubernetes.io/name" : local.name
    }, var.labels)
  }
  rule {
    api_groups = [""]
    resources  = ["secrets", "configmaps"]
    verbs      = ["create", "get", "list", "watch", "update", "patch", "delete"]
  }
  rule {
    api_groups = [""]
    resources  = ["events"]
    verbs      = ["create", "list"]
  }
}