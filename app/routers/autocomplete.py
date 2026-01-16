from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.config import EQUIPMENT_TYPES

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/movements", response_class=HTMLResponse)
async def search_movements(
    request: Request,
    movement: str = Query("", alias="movement"),
    equipment_type: str = Query("", alias="equipment_type"),
    weight: str = Query("", alias="weight"),
    n_of_reps: str = Query("", alias="n_of_reps"),
):
    """Search movements for autocomplete."""
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
        "partials/autocomplete_results.html",
        {
            "request": request,
            "results": movements,
            "input_name": "movement",
            "current_movement": movement,
            "current_equipment": equipment_type,
            "current_weight": weight,
            "current_reps": n_of_reps,
        },
    )


@router.get("/equipment", response_class=HTMLResponse)
async def search_equipment(
    request: Request,
    movement: str = Query("", alias="movement"),
    equipment_type: str = Query("", alias="equipment_type"),
    weight: str = Query("", alias="weight"),
    n_of_reps: str = Query("", alias="n_of_reps"),
):
    """Search equipment types for autocomplete."""
    q = equipment_type.lower().strip()

    if not q:
        return HTMLResponse(content="")

    # Filter from predefined list + any custom ones in DB
    db = get_db()
    result = db.execute(
        "SELECT name FROM equipment_types WHERE name LIKE ? LIMIT 10",
        [f"%{q}%"],
    )
    rows = result.fetchall()
    equipment = [row[0] for row in rows]

    # Also include predefined types that match
    for eq in EQUIPMENT_TYPES:
        if q in eq.lower() and eq not in equipment:
            equipment.append(eq)

    return templates.TemplateResponse(
        "partials/autocomplete_results.html",
        {
            "request": request,
            "results": equipment[:10],
            "input_name": "equipment_type",
            "current_movement": movement,
            "current_equipment": equipment_type,
            "current_weight": weight,
            "current_reps": n_of_reps,
        },
    )


@router.post("/select", response_class=HTMLResponse)
async def select_autocomplete(
    request: Request,
    field: str = Form(...),
    value: str = Form(...),
    movement: str = Form(""),
    equipment_type: str = Form(""),
    weight: str = Form(""),
    n_of_reps: str = Form(""),
):
    """Handle autocomplete selection - return form with selected value filled in."""
    # Update the appropriate field with the selected value
    if field == "movement":
        movement = value
    elif field == "equipment_type":
        equipment_type = value

    return templates.TemplateResponse(
        "partials/logger_form_inner.html",
        {
            "request": request,
            "movement_value": movement,
            "equipment_type_value": equipment_type,
            "weight_value": weight,
            "n_of_reps_value": n_of_reps,
        },
    )
