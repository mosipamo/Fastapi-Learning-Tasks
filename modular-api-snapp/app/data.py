users: list[dict] = [
    {"id": 1, "name": "Sara Ahmadi", "role": "passenger", "city": "Tehran"},
    {"id": 2, "name": "Kaveh Rezaei", "role": "driver", "city": "Tehran"},
    {"id": 3, "name": "Negar Karimi", "role": "passenger", "city": "Mashhad"},
    {"id": 4, "name": "Arian Mousavi", "role": "driver", "city": "Mashhad"},
    {"id": 5, "name": "Bahar Sadeghi", "role": "passenger", "city": "Shiraz"},
    {"id": 6, "name": "Pouya Naderi", "role": "driver", "city": "Shiraz"},
    {"id": 7, "name": "Yasaman Tavakoli", "role": "passenger", "city": "Isfahan"},
    {"id": 8, "name": "Mehrshad Bahrami", "role": "driver", "city": "Isfahan"},
]

rides: list[dict] = [
    {"id": 101, "passenger_id": 1, "driver_id": 2, "origin": "Vanak", "destination": "Tajrish", "status": "completed", "fare": 185000},
    {"id": 102, "passenger_id": 3, "driver_id": 4, "origin": "Vakil Abad", "destination": "Ferdowsi Square", "status": "ongoing", "fare": 120000},
    {"id": 103, "passenger_id": 5, "driver_id": 6, "origin": "Zand", "destination": "Eram Garden", "status": "requested", "fare": 95000},
    {"id": 104, "passenger_id": 7, "driver_id": 8, "origin": "Naghsh-e Jahan", "destination": "Si-o-se-pol", "status": "completed", "fare": 140000},
    {"id": 105, "passenger_id": 1, "driver_id": 2, "origin": "Tajrish", "destination": "Vanak", "status": "cancelled", "fare": 0},
    {"id": 106, "passenger_id": 3, "driver_id": 4, "origin": "Ferdowsi Square", "destination": "Vakil Abad", "status": "completed", "fare": 130000},
    {"id": 107, "passenger_id": 5, "driver_id": 6, "origin": "Eram Garden", "destination": "Zand", "status": "ongoing", "fare": 88000},
    {"id": 108, "passenger_id": 7, "driver_id": 8, "origin": "Si-o-se-pol", "destination": "Naghsh-e Jahan", "status": "requested", "fare": 0},
]


def get_user(user_id: int) -> dict | None:
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def get_ride(ride_id: int) -> dict | None:
    for ride in rides:
        if ride["id"] == ride_id:
            return ride
    return None
