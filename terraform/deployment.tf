

resource "kubernetes_namespace" "namespace" {
  metadata {
    name = local.name
  }
}

resource "kubernetes_deployment" "deployment" {
  metadata {
    name      = local.name
    namespace = kubernetes_namespace.namespace.metadata.0.name
  }
  spec {
    replicas = var.replica_count
    selector {
      match_labels = {
        "app.kubernetes.io/name" : local.name
      }
    }
    template {
      metadata {
        labels = merge({
          "app.kubernetes.io/name" : local.name
        }, var.labels)
      }
      spec {
        service_account_name            = kubernetes_service_account.service_account.metadata.0.name
        automount_service_account_token = false
        container {
          name              = local.name
          image             = var.image
          image_pull_policy = var.image_pull_policy
          env {
            name  = "BIND_IP"
            value = var.bind_ip
          }
          env {
            name  = "BIND_PORT"
            value = var.bind_port
          }
          env {
            name  = "DEBUG_PAUL"
            value = tostring(var.debug_enabled)
          }
          env {
            name  = "K8S_ENDPOINT"
            value = var.kubernetes_endpoint
          }
          port {
            container_port = var.bind_port
          }
          resources {
            requests = {
              cpu    = var.cpu_request
              memory = var.memory_request
            }
            limits = {
              cpu    = var.cpu_limit
              memory = var.memory_limit
            }
          }
          liveness_probe {
            http_get {
              path = "/healthz"
              port = 8080
            }
            initial_delay_seconds = 30
            period_seconds        = 5
          }
          readiness_probe {
            http_get {
              path = "/healthz"
              port = 8080
            }
            initial_delay_seconds = 30
            period_seconds        = 30
          }
          volume_mount {
            name       = "service-token"
            mount_path = "/var/run/secrets/kubernetes.io/serviceaccount/"
            read_only  = true
          }
        }
        volume {
          name = "service-token"
          secret {
            secret_name = kubernetes_service_account.service_account.default_secret_name
          }
        }
      }
    }
  }
}