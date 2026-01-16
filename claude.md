# Exercise Companion

A FastAPI web application for tracking and visualizing workout data.

## Tech Stack

- **Framework**: FastAPI with Jinja2 templates
- **Database**: Turso (libsql) with local replica sync
- **Package Manager**: uv

## Project Structure

```
app/
├── main.py           # FastAPI app entry point
├── config.py         # Environment configuration
├── database.py       # Turso/libsql connection and schema
├── models/
│   └── schemas.py    # Pydantic models
├── routers/
│   ├── exercises.py      # CRUD for exercise sets
│   ├── autocomplete.py   # Movement/equipment autocomplete
│   ├── visualizer.py     # Data visualization endpoints
│   ├── workout_summary.py # Workout summaries
│   └── import_data.py    # Data import functionality
├── services/
│   └── aggregation.py    # Data aggregation logic
└── templates/            # Jinja2 HTML templates
```

## Database Schema

- **movements**: Exercise movement names
- **equipment_types**: Equipment categories (dumbbell, barbell, etc.)
- **weightlifting_set**: Weight training logs (movement, equipment, reps, weight)
- **cardio_set**: Cardio logs (movement, equipment, distance, duration, power)

## Running Locally

```bash
# Install dependencies
uv sync

# Set environment variables (copy .env.example to .env)
cp .env.example .env
# Edit .env with your Turso credentials

# Run development server
uv run python -m uvicorn app.main:app --reload
```

## Environment Variables

- `TURSO_DATABASE_URL`: Turso database URL (libsql://...)
- `TURSO_AUTH_TOKEN`: Turso authentication token

## API Routes

- `GET /` - Main page
- `/api/exercises` - Exercise CRUD operations
- `/api/autocomplete` - Autocomplete for movements/equipment
- `/api/visualizer` - Data visualization
- `/api/summary` - Workout summaries
- `/api/import` - Data import
