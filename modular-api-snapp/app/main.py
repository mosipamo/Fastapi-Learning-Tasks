from fastapi import FastAPI

from app.data import rides, users
from app.routers import rides as rides_router
from app.routers import users as users_router

app = FastAPI(title="Snapp Modular API")


@app.get("/")
async def welcome():
    return {"service": "Snapp", "users_count": len(users), "rides_count": len(rides)}


app.include_router(users_router.router)
app.include_router(rides_router.router)
