import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api import api_router
from app.core.config import settings
from app.core.constants import ALLOWED_HEADERS, ALLOWED_METHODS
from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.logging_utils import setup_logger

# Initialize application-wide logging
logger = setup_logger("app")
# Ensure uvicorn access logs use our configuration
logging.getLogger("uvicorn.access").handlers = logger.handlers

app = FastAPI(title="HireHub Backend", version="1.0.0")


# Add request/response logging middleware
app.add_middleware(LoggingMiddleware)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


app.include_router(api_router, prefix="/api/v1")
