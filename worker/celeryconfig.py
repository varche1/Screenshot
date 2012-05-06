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

# Max task executing time(soft)
CELERYD_TASK_SOFT_TIME_LIMIT = 45

# Max task executing time(hard)
CELERYD_TASK_TIME_LIMIT = 60

# Screen option
SCREENSHOT_THUMB_SIZE = {"width": 100, "height": 100}
SCREENSHOT_MEDIUM_SIZE = {"width": 800, "height": 0}
SCREENSHOT_ORIGINAL_SIZE = {"width": 0, "height": 0}
SCREENSHOT_QUALITY = 90

# Update options
BASE_WORKER_URL = 'https://raw.github.com/stepler/Screenshot/master/worker/worker_base.py'
BASE_WORKER_MODULE = 'worker_base.py'

CELERYCONFIG_URL = 'https://raw.github.com/stepler/Screenshot/master/worker/celeryconfig.py'
CELERYCONFIG_MODULE = 'celeryconfig.py'