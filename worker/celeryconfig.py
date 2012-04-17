# Broker settings
BROKER_HOST = "176.9.24.81"
BROKER_PORT = 5672
BROKER_USER = "celery"
BROKER_PASSWORD = "lemon"
BROKER_VHOST = "celeryhost"

# Backend settings
CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "176.9.24.81",
    "port": 27017,
    "user": "celeryuser",
    "password": "lemon",
    "database": "celery",
    "taskmeta_collection": "celery_result",
}

# Additional settings
CELERY_IMPORTS = ("worker", "worker_base") 