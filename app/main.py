import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api import api_router
from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.logging_utils import setup_logger

# Initialize logging
logger = setup_logger("app")
logging.getLogger("uvicorn.access").handlers = logger.handlers

app = FastAPI(title="HireHub Backend", version="1.0.0",root_path="/api")

# ✅ Correct CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # your frontend dev server
        "http://127.0.0.1:5173",      # sometimes React/Vite uses this
        "http://0.0.0.0:5173",        # optional for Docker/EC2 setups
    ],
    allow_credentials=True,
    allow_methods=["*"],  # or ["GET", "POST", "OPTIONS"]
    allow_headers=["*"],  # include "Content-Type", "Authorization", etc.
)

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Include routers
app.include_router(api_router, prefix="/api/v1")
