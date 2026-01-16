from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.config import EQUIPMENT_TYPES
from app.services.aggregation import aggregate_by_date

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def get_visualizer(request: Request):
    """Return the visualizer page."""
    content = templates.TemplateResponse(
        "partials/visualizer.html", {"request": request}
    ).body.decode()

    tabs = templates.TemplateResponse(
        "partials/tabs.html", {"request": request, "active_tab": "history"}
    ).body.decode()

    return HTMLResponse(
        content=content + f'<div id="tabs-container" hx-swap-oob="innerHTML">{tabs}</div>'
    )


@router.get("/autocomplete", response_class=HTMLResponse)
async def visualizer_autocomplete(request: Request, movement: str = Query("")):
    """Search movements for visualizer autocomplete."""
    db = get_db()
    q = movement.lower().strip()

    if not q:
        return HTMLResponse(content="")

    result = db.execute(
        "SELECT name FROM movements WHERE name LIKE ? LIMIT 10",
        [f"%{q}%"],
    )
    rows = result.fetchall()
    movements = [row[0] for row in rows]

    return templates.TemplateResponse(
        "partials/visualizer_autocomplete.html",
        {"request": request, "results": movements},
    )


@router.get("/search", response_class=HTMLResponse)
async def search_by_movement(request: Request, movement: str = Query(...)):
    """Search weightlifting sets by movement and return aggregated data."""
    db = get_db()
    movement = movement.lower().strip()

    result = db.execute(
        """
        SELECT id, movement, equipment_type, timestamp, n_of_reps, weight
        FROM weightlifting_set
        WHERE movement = ?
        ORDER BY timestamp DESC
        """,
        [movement],
    )
    rows = result.fetchall()

    # Convert to list of dicts
    sets = []
    for row in rows:
        sets.append({
            "id": row[0],
            "movement": row[1],
            "equipment_type": row[2],
            "timestamp": row[3],
            "n_of_reps": row[4],
            "weight": row[5],
        })

    # Aggregate by date
    aggregated = aggregate_by_date(sets)

    return templates.TemplateResponse(
        "partials/visualizer_table.html",
        {"request": request, "aggregated_data": aggregated},
    )


@router.get("/edit/{set_id}", response_class=HTMLResponse)
async def get_edit_modal(request: Request, set_id: int):
    """Return the edit modal for a specific set."""
    db = get_db()

    result = db.execute(
        """
        SELECT id, movement, equipment_type, timestamp, n_of_reps, weight
        FROM weightlifting_set
        WHERE id = ?
        """,
        [set_id],
    )
    row = result.fetchone()

    if not row:
        return HTMLResponse(content="<p>Set not found</p>", status_code=404)

    set_data = {
        "id": row[0],
        "movement": row[1],
        "equipment_type": row[2],
        "timestamp": row[3],
        "n_of_reps": row[4],
        "weight": row[5],
    }

    return templates.TemplateResponse(
        "partials/edit_modal.html",
        {"request": request, "set": set_data, "equipment_types": EQUIPMENT_TYPES},
    )
