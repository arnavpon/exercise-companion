from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.routers import exercises, autocomplete, visualizer, workout_summary, import_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    yield


app = FastAPI(title="Exercise Mentor", lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
app.include_router(autocomplete.router, prefix="/api/autocomplete", tags=["autocomplete"])
app.include_router(visualizer.router, prefix="/api/visualizer", tags=["visualizer"])
app.include_router(workout_summary.router, prefix="/api/summary", tags=["summary"])
app.include_router(import_data.router, prefix="/api/import", tags=["import"])


@app.get("/")
async def index(request: Request):
    """Render the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/dismiss")
async def dismiss_notification():
    """Dismiss a notification - returns empty string to remove element."""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content="")
