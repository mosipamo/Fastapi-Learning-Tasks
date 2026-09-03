from fastapi import FastAPI

from models import LoginRequest, SignupRequest
from store import (
    accounts,
    add_account,
    count_accounts,
    find_usernames,
    get_account,
    has_user,
)

app = FastAPI(title="Namava Signup")


@app.get("/")
def read_root():
    return {
        "message": "Namava signup service",
        "accounts_count": count_accounts(),
    }


@app.post("/signup")
def signup(request: SignupRequest):
    flag = True
    if has_user(request.username):
        flag = False
    add_account(request.model_dump())

    return {
        "username": request.username,
        "email": request.email,
        "age": request.age if request.age else None,
        "roles": request.roles if request.roles else ["user"],
        "is_new": flag,
    }


@app.get("/accounts")
def read_accounts(prefix: str | None = None, limit: int | None = None):
    usernames = find_usernames(prefix)
    if limit is not None:
        usernames = usernames[:limit]
    return {
        "count": len(usernames),
        "usernames": usernames,
        "total": count_accounts(),
    }


@app.get("/accounts/{username}")
def read_account(username: str):
    account = get_account(username)
    if account is None:
        return {"username": "nobody", "found": False}
    return {
    	"username": account["username"],
    	"email": account["email"],
        "age": account["age"],
        "roles": account["roles"],
        "found": True,
    }


@app.post("/login")
def login(request: LoginRequest):
    account = get_account(request.username)
    if account is None or account["password"] != request.password:
        return {
            "username": request.username,
            "authenticated": False,
        }
    return {
        "username": request.username,
        "authenticated": True,
    }
