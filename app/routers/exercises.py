from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/form", response_class=HTMLResponse)
async def get_form(request: Request):
    """Return the exercise logging form."""
    content = templates.TemplateResponse(
        "partials/logger_form.html", {"request": request}
    ).body.decode()

    tabs = templates.TemplateResponse(
        "partials/tabs.html", {"request": request, "active_tab": "logger"}
    ).body.decode()

    return HTMLResponse(
        content=content + f'<div id="tabs-container" hx-swap-oob="innerHTML">{tabs}</div>'
    )


@router.post("/weightlifting", response_class=HTMLResponse)
async def create_weightlifting_set(
    request: Request,
    movement: str = Form(...),
    equipment_type: str = Form(...),
    weight: float = Form(...),
    n_of_reps: int = Form(...),
):
    """Create a new weightlifting set."""
    db = get_db()

    # Normalize inputs
    movement = movement.lower().strip()
    equipment_type = equipment_type.lower().strip()

    # Ensure movement exists in movements table
    existing = db.execute(
        "SELECT id FROM movements WHERE name = ?", [movement]
    ).fetchone()
    if not existing:
        db.execute("INSERT INTO movements (name) VALUES (?)", [movement])

    # Ensure equipment_type exists in equipment_types table
    existing = db.execute(
        "SELECT id FROM equipment_types WHERE name = ?", [equipment_type]
    ).fetchone()
    if not existing:
        db.execute("INSERT INTO equipment_types (name) VALUES (?)", [equipment_type])

    # Insert the weightlifting set
    db.execute(
        """
        INSERT INTO weightlifting_set (movement, equipment_type, weight, n_of_reps)
        VALUES (?, ?, ?, ?)
        """,
        [movement, equipment_type, weight, n_of_reps],
    )

    # Return cleared form with success message
    return templates.TemplateResponse(
        "partials/form_success.html", {"request": request}
    )


@router.put("/weightlifting/{set_id}", response_class=HTMLResponse)
async def update_weightlifting_set(
    request: Request,
    set_id: int,
    movement: str = Form(...),
    equipment_type: str = Form(...),
    weight: float = Form(...),
    n_of_reps: int = Form(...),
):
    """Update an existing weightlifting set."""
    db = get_db()

    # Normalize inputs
    movement = movement.lower().strip()
    equipment_type = equipment_type.lower().strip()

    # Update the record (preserving timestamp)
    db.execute(
        """
        UPDATE weightlifting_set
        SET movement = ?, equipment_type = ?, weight = ?, n_of_reps = ?
        WHERE id = ?
        """,
        [movement, equipment_type, weight, n_of_reps, set_id],
    )

    # Return success message (modal will close)
    return templates.TemplateResponse(
        "partials/edit_success.html", {"request": request}
    )


@router.delete("/weightlifting/{set_id}", response_class=HTMLResponse)
async def delete_weightlifting_set(set_id: int):
    """Delete a weightlifting set."""
    db = get_db()
    db.execute("DELETE FROM weightlifting_set WHERE id = ?", [set_id])
    return HTMLResponse(content="", status_code=200)
