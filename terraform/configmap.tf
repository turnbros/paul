resource "kubernetes_config_map" "configmap" {
  metadata {
    name      = var.configmap_name
    namespace = kubernetes_namespace.namespace.metadata.0.name
    labels = merge({
        "app.kubernetes.io/name" : local.name
    }, var.labels)
  }
  data = var.pauls_config
}