EVENTS: list[tuple[str, int]] = []

MENU: dict[int, dict] = {
    1: {"id": 1, "name": "Pizza Margherita", "price": 1850000},
    2: {"id": 2, "name": "Chicken Burger", "price": 1450000},
    3: {"id": 3, "name": "Caesar Salad", "price": 980000},
    4: {"id": 4, "name": "Mushroom Soup", "price": 620000},
    5: {"id": 5, "name": "Lentil Stew", "price": 1100000},
}


class Connection:

    _next_id = 1

    def __init__(self) -> None:
        self._id = Connection._next_id
        Connection._next_id += 1

        self.open = True
        EVENTS.append(("open", self._id))

    def fetch_item(self, item_id: int) -> dict | None:
        if not self.open:
            raise ValueError("Connection is closed")

        return MENU.get(item_id)

    def fetch_page(self, offset: int, size: int) -> list[dict]:
        if not self.open:
            raise ValueError("Connection is closed")

        return [
            MENU[i]
            for i in range(offset + 1, offset + size + 1)
            if i in MENU
        ]

    def close(self) -> None:
        if not self.open:
            return

        self.open = False
        EVENTS.append(("close", self._id))


def reset_events() -> None:
    EVENTS.clear()
    Connection._next_id = 1


def get_connection():
    conn = Connection()
    try:
        yield conn
    finally:
        conn.close()
