from data import orders, users


def orders_of_user(user_id: int) -> list[dict]:
    return [order for order in orders.values() if order["user_id"] == user_id]


def user_summary(user_id: int) -> dict:
    user_orders = orders_of_user(user_id)
    return {
        "user_id": user_id,
        "name": users[user_id]["name"],
        "is_plus": users[user_id]["is_plus"],
        "order_count": len(user_orders),
        "total_amount": sum(order["amount"] for order in user_orders),
    }
