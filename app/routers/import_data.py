import json
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def get_import_form(request: Request):
    """Return the import form."""
    content = templates.TemplateResponse(
        "partials/import_form.html", {"request": request}
    ).body.decode()

    tabs = templates.TemplateResponse(
        "partials/tabs.html", {"request": request, "active_tab": "import"}
    ).body.decode()

    return HTMLResponse(
        content=content + f'<div id="tabs-container" hx-swap-oob="innerHTML">{tabs}</div>'
    )


@router.post("", response_class=HTMLResponse)
async def import_data(request: Request, json_data: str = Form(...)):
    """Import data from JSON export."""
    db = get_db()

    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        return HTMLResponse(
            content=f'<div class="notification is-danger">Invalid JSON: {str(e)}</div>',
            status_code=400,
        )

    movements_count = 0
    equipment_count = 0
    weightlifting_count = 0
    cardio_count = 0

    # Import movements
    for movement in data.get("movements", []):
        try:
            db.execute(
                "INSERT OR IGNORE INTO movements (name) VALUES (?)",
                [movement["name"].lower().strip()],
            )
            movements_count += 1
        except Exception:
            pass

    # Import equipment types
    for equipment in data.get("equipmentTypes", []):
        try:
            db.execute(
                "INSERT OR IGNORE INTO equipment_types (name) VALUES (?)",
                [equipment["name"].lower().strip()],
            )
            equipment_count += 1
        except Exception:
            pass

    # Import weightlifting sets
    for ws in data.get("weightliftingSets", []):
        try:
            db.execute(
                """
                INSERT INTO weightlifting_set (movement, equipment_type, timestamp, n_of_reps, weight)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    ws["movement"].lower().strip(),
                    ws["equipmentType"].lower().strip(),
                    ws["timestamp"],
                    ws["nOfReps"],
                    ws["weight"],
                ],
            )
            weightlifting_count += 1
        except Exception as e:
            print(f"Error importing weightlifting set: {e}")

    # Import cardio sets
    for cs in data.get("cardioSets", []):
        try:
            db.execute(
                """
                INSERT INTO cardio_set (movement, equipment_type, timestamp, distance, duration, power_output)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    cs["movement"].lower().strip(),
                    cs["equipmentType"].lower().strip(),
                    cs["timestamp"],
                    cs["distance"],
                    cs["duration"],
                    cs.get("powerOutput", 0),
                ],
            )
            cardio_count += 1
        except Exception as e:
            print(f"Error importing cardio set: {e}")

    return templates.TemplateResponse(
        "partials/import_success.html",
        {
            "request": request,
            "movements_count": movements_count,
            "equipment_count": equipment_count,
            "weightlifting_count": weightlifting_count,
            "cardio_count": cardio_count,
        },
    )
