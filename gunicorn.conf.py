import os

# Configuración optimizada para Railway
bind = f"0.0.0.0:{os.getenv('PORT', 8080)}"
workers = 2  # Railway tiene CPU limitada en free tier
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True  # Importante: precarga la app
accesslog = "-"
errorlog = "-"
