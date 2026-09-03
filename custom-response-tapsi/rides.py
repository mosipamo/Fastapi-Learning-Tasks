STATUS_FLOW = {"requested": "ongoing", "ongoing": "completed"}


def build_ride(new_id: int, origin: str, destination: str, price: int) -> dict:
    return {
        "id": new_id,
        "origin": origin,
        "destination": destination,
        "price": price,
        "status": "requested",
    }


def ride_headers(ride_id: int) -> dict[str, str]:
    return {
        "Location": f"/rides/{ride_id}",
        "X-Ride-Id": str(ride_id),
    }


def validate_new_ride(payload: dict) -> str | None:
    if "origin" not in payload or "destination" not in payload or "price" not in payload:
        return "missing required fields"
    if not isinstance(payload["origin"], str) or not isinstance(payload["destination"], str):
        return "origin and destination must be strings"
    if not payload["origin"].strip() or not payload["destination"].strip():
        return "origin and destination cannot be empty"
    if isinstance(payload["price"], bool) or not isinstance(payload["price"], int) or payload["price"] <= 0:
        return "price must be a positive integer"
    return None


def next_status(current: str) -> str | None:
    return STATUS_FLOW.get(current)
