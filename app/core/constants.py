ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:5173",
]

ALLOWED_METHODS = ["GET", "POST", "PUT", "OPTIONS"]

ALLOWED_HEADERS = [
    "Accept",
    "Accept-Language",
    "Authorization",
    "Content-Language",
    "Content-Type",
    "Cache-Control",
    "X-Requested-With",
]

LOG_TO_FILE = True
LOG_LEVEL = "INFO"
LOG_FILE_NAME = "system.log"
ERROR_LOG_FILE_NAME = "errors.log"
