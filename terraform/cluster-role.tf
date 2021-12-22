resource "kubernetes_cluster_role" "cluster_role" {
  metadata {
    name = local.name
    labels = merge({
      "app.kubernetes.io/name" : local.name
    }, var.labels)
  }
  rule {
    api_groups = ["*"]
    resources  = ["*"]
    verbs      = ["get", "patch", "delete"]
  }
  rule {
    api_groups = [""]
    resources  = ["events"]
    verbs      = ["list"]
  }
  rule {
    api_groups = [""]
    resources  = ["pod", "pods/log"]
    verbs      = ["get"]
  }
}