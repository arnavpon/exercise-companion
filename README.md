# Exercise Companion

A fitness tracking web app built with FastAPI, HTMX, Bulma CSS, and Turso (SQLite).

## Setup

1. Copy the environment template and add your Turso credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your Turso database URL and auth token
   ```

2. Run the server:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

3. Open http://localhost:8000 in your browser

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
