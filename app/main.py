import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api import api_router
from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.logging_utils import setup_logger

# ----------------------------
# Logging Configuration
# ----------------------------
logger = setup_logger("app")
logging.getLogger("uvicorn.access").handlers = logger.handlers

# ----------------------------
# FastAPI App Initialization
# ----------------------------
app = FastAPI(title="HireHub Backend", version="1.0.0")

# Add request/response logging middleware
app.add_middleware(LoggingMiddleware)

# ----------------------------
# CORS Configuration
# ----------------------------
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Your frontend URL
    # Add deployed frontend URLs here if needed
]

ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
ALLOWED_HEADERS = ["*"]  # Allow all headers like Content-Type, Authorization

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)

# ----------------------------
# Templates Configuration
# ----------------------------
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# ----------------------------
# API Router
# ----------------------------
app.include_router(api_router, prefix="/api/v1")
