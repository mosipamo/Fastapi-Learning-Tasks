from fastapi import FastAPI

from data import orders, users
from helpers import orders_of_user, user_summary

app = FastAPI(title="Digikala Internal Panel")


@app.get("/")
def welcome():
    return {
        "message": "Digikala internal user panel",
        "users_count": len(users),
        "orders_count": len(orders),
    }


@app.get("/users")
def list_users():
    return list(users.values())


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return users[user_id]


@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int):
    return orders_of_user(user_id)


@app.get("/users/{user_id}/orders/{order_id}")
def read_order(user_id: int, order_id: int):
    return orders[order_id]


@app.get("/users/{user_id}/summary")
def read_user_summary(user_id: int):
    return user_summary(user_id)
