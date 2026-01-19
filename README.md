# Exercise Companion

A fitness tracking web app built with FastAPI, HTMX, Bulma CSS, and Turso (SQLite).

## Setup

Create a `.env` file with your Turso credentials:
```
TURSO_DATABASE_URL=libsql://your-db.turso.io
TURSO_AUTH_TOKEN=your-token
```

### Option 1: Docker (Recommended)

```bash
docker build -t exercise-companion .
docker run --rm -p 8000:8000 --env-file .env exercise-companion
```

### Option 2: Local Development

```bash
uv sync
uv run python -m uvicorn app.main:app --reload
```

Regardless of run mode, open http://localhost:8000 in your browser to use app. 

## Features

- **Log Workout**: Record weightlifting sets with movement, equipment type, weight, and reps
- **Summary**: View your current or last workout with totals
- **History**: Search and view exercise history aggregated by date
- **Import**: Import data from the Flutter app export (JSON format)

## Tech Stack

- **FastAPI** - Python web framework
- **HTMX** - HTML over the wire (no JavaScript)
- **Bulma CSS** - Modern CSS framework
- **Turso** - Hosted SQLite database
- **Jinja2** - Server-side templates