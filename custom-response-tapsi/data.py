rides: list[dict] = [
    {"id": 1, "origin": "Tajrish", "destination": "Vanak", "price": 145000, "status": "completed"},
    {"id": 2, "origin": "Azadi", "destination": "Enghelab", "price": 98000, "status": "completed"},
    {"id": 3, "origin": "Saadat Abad", "destination": "Jordan", "price": 132000, "status": "ongoing"},
]


def next_ride_id() -> int:
    if not rides:
        return 1
    return max(r["id"] for r in rides) + 1


def find_ride(ride_id: int) -> dict | None:
    for r in rides:
        if r["id"] == ride_id:
            return r
    return None
