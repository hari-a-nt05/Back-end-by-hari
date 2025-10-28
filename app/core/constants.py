ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

ALLOWED_HEADERS = [
    "Accept",
    "Accept-Language",
    "Authorization",
    "Content-Language",
    "Content-Type",
    "Cache-Control",
    "X-Requested-With",
    "Origin",
    "Access-Control-Request-Method",
    "Access-Control-Request-Headers",
]

LOG_TO_FILE = True
LOG_LEVEL = "INFO"
LOG_FILE_NAME = "system.log"
ERROR_LOG_FILE_NAME = "errors.log"
