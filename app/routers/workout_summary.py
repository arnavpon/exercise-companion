from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Workout session threshold (2 hours)
WORKOUT_SESSION_THRESHOLD = timedelta(hours=2)


def _render_with_tabs(request: Request, template_name: str, context: dict):
    """Helper to render content with tabs OOB swap."""
    content = templates.TemplateResponse(template_name, context).body.decode()
    tabs = templates.TemplateResponse(
        "partials/tabs.html", {"request": request, "active_tab": "summary"}
    ).body.decode()
    return HTMLResponse(
        content=content + f'<div id="tabs-container" hx-swap-oob="innerHTML">{tabs}</div>'
    )


@router.get("", response_class=HTMLResponse)
async def get_workout_summary(request: Request):
    """Get current or last workout summary."""
    db = get_db()
    now = datetime.now()

    # Get most recent set
    result = db.execute(
        """
        SELECT id, movement, equipment_type, timestamp, n_of_reps, weight
        FROM weightlifting_set
        ORDER BY timestamp DESC
        LIMIT 1
        """
    )
    latest = result.fetchone()

    if not latest:
        return _render_with_tabs(
            request,
            "partials/workout_summary.html",
            {
                "request": request,
                "is_current": False,
                "start_time": None,
                "total_minutes": 0,
                "exercises": {},
            },
        )

    latest_timestamp = latest[3]
    if isinstance(latest_timestamp, str):
        latest_timestamp = datetime.fromisoformat(latest_timestamp.replace("Z", ""))

    # Determine if this is a "current" workout (within 2 hours)
    is_current = (now - latest_timestamp) < WORKOUT_SESSION_THRESHOLD

    # Get all sets belonging to this workout session
    # Work backwards from the latest set, including sets within 2 hours of each other
    workout_sets = []
    current_set = latest
    session_end_time = latest_timestamp

    # Get all sets ordered by timestamp descending
    all_sets_result = db.execute(
        """
        SELECT id, movement, equipment_type, timestamp, n_of_reps, weight
        FROM weightlifting_set
        ORDER BY timestamp DESC
        """
    )
    all_sets = all_sets_result.fetchall()

    # Group sets into the same workout session
    prev_timestamp = None
    for row in all_sets:
        ts = row[3]
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts.replace("Z", ""))

        if prev_timestamp is None:
            # First set - include it
            workout_sets.append(row)
            prev_timestamp = ts
        else:
            # Check if within 2 hours of previous set
            if (prev_timestamp - ts) < WORKOUT_SESSION_THRESHOLD:
                workout_sets.append(row)
                prev_timestamp = ts
            else:
                # This set belongs to a different workout
                break

    if not workout_sets:
        return _render_with_tabs(
            request,
            "partials/workout_summary.html",
            {
                "request": request,
                "is_current": False,
                "start_time": None,
                "total_minutes": 0,
                "exercises": {},
            },
        )

    # Calculate start time and duration
    timestamps = []
    for row in workout_sets:
        ts = row[3]
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts.replace("Z", ""))
        timestamps.append(ts)

    start_time = min(timestamps)
    end_time = max(timestamps)
    total_minutes = int((end_time - start_time).total_seconds() / 60)

    # Aggregate by exercise
    exercises = {}
    for row in workout_sets:
        movement = row[1]
        weight = row[5]
        reps = row[4]

        if movement not in exercises:
            exercises[movement] = {"total_weight": 0.0, "count": 0}

        exercises[movement]["total_weight"] += weight * reps
        exercises[movement]["count"] += 1

    return _render_with_tabs(
        request,
        "partials/workout_summary.html",
        {
            "request": request,
            "is_current": is_current,
            "start_time": start_time,
            "total_minutes": total_minutes,
            "exercises": exercises,
        },
    )
