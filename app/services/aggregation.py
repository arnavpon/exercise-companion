from typing import List, Dict
from datetime import datetime

EQUIPMENT_BODYWEIGHT = "bodyweight"
EQUIPMENT_DUMBBELL = "dumbbell"


def calculate_total_weight(sets: List[dict]) -> tuple[float, int]:
    """
    Calculate total weight moved based on equipment type.

    Returns: (total_weight, bodyweight_reps)
    - Bodyweight: returns total reps only (weight is 0)
    - Dumbbells: doubles weight (one in each hand)
    - Others: weight x reps
    """
    total_weight = 0.0
    bodyweight_reps = 0

    for s in sets:
        eq_type = s["equipment_type"].lower()
        weight = s["weight"]
        reps = s["n_of_reps"]

        if eq_type == EQUIPMENT_BODYWEIGHT:
            bodyweight_reps += reps
        elif eq_type == EQUIPMENT_DUMBBELL:
            # Double for dumbbells (both hands)
            total_weight += weight * reps * 2
        else:
            # Standard: weight x reps
            total_weight += weight * reps

    return total_weight, bodyweight_reps


def calculate_time_elapsed(sets: List[dict]) -> str:
    """Calculate time between first and last set."""
    if not sets:
        return "0m 0s"

    timestamps = []
    for s in sets:
        ts = s["timestamp"]
        if isinstance(ts, str):
            # Handle ISO format with or without timezone
            ts = ts.replace("Z", "+00:00")
            if "+" not in ts and "-" not in ts[10:]:
                ts = datetime.fromisoformat(ts)
            else:
                ts = datetime.fromisoformat(ts)
        timestamps.append(ts)

    if len(timestamps) < 2:
        return "0m 0s"

    timestamps.sort()
    delta = timestamps[-1] - timestamps[0]
    total_seconds = int(delta.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes}m {seconds}s"


def format_total_display(
    total_weight: float, bodyweight_reps: int, time_elapsed: str
) -> str:
    """Format the display string for total weight/reps."""
    if total_weight == 0 and bodyweight_reps > 0:
        return f"{bodyweight_reps} reps in {time_elapsed}"
    elif bodyweight_reps == 0 and total_weight > 0:
        return f"{total_weight:.2f} lbs in {time_elapsed}"
    elif bodyweight_reps > 0 and total_weight > 0:
        return f"{bodyweight_reps} reps + {total_weight:.2f} lbs in {time_elapsed}"
    return f"0 in {time_elapsed}"


def aggregate_by_date(sets: List[dict]) -> List[Dict]:
    """
    Group sets by date and calculate aggregates.
    Returns list sorted by date descending.
    """
    by_date = {}

    for s in sets:
        ts = s["timestamp"]
        if isinstance(ts, str):
            ts = ts.replace("Z", "+00:00")
            if "+" not in ts and "-" not in ts[10:]:
                ts = datetime.fromisoformat(ts)
            else:
                ts = datetime.fromisoformat(ts)

        date_key = ts.strftime("%Y-%m-%d")

        if date_key not in by_date:
            by_date[date_key] = []
        by_date[date_key].append(s)

    result = []
    for date_str, date_sets in sorted(by_date.items(), reverse=True):
        # Sort sets within date by timestamp descending
        date_sets.sort(
            key=lambda x: (
                x["timestamp"]
                if isinstance(x["timestamp"], datetime)
                else datetime.fromisoformat(x["timestamp"].replace("Z", "+00:00"))
            ),
            reverse=True,
        )

        total_weight, bodyweight_reps = calculate_total_weight(date_sets)
        time_elapsed = calculate_time_elapsed(date_sets)
        display = format_total_display(total_weight, bodyweight_reps, time_elapsed)

        # Format date for display
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        display_date = dt.strftime("%m/%d/%Y")

        result.append(
            {
                "date": display_date,
                "movement": date_sets[0]["movement"],
                "total_weight_or_reps": display,
                "time_elapsed": time_elapsed,
                "sets": date_sets,
            }
        )

    return result
