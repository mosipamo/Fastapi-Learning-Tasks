from this import s

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from data import find_movie, find_user, movies
from errors import FilimoError, error_body

app = FastAPI(title="Filimo Streaming Service")


@app.exception_handler(FilimoError)
def handle_filimo_error(request: Request, exc: FilimoError):

    return JSONResponse(
        status_code=exc.status_code,
        content=error_body(exc.code, exc.message),
        headers={"X-Error-Code": exc.code},
    )

@app.get("/")
async def root():
    return {
        "message": "Filimo streaming service",
        "movies_count": len(movies),
    }


@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie


@app.get("/movies/{movie_id}/play")
async def play_movie(movie_id: int, user_id: int):
    movie = find_movie(movie_id)
    user = find_user(user_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if movie["required_tier"] == "premium" and user["tier"] == "free":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="premium subscription required")
    if user["age"] < movie["min_age"]:
        raise FilimoError(code="age_restricted", message="this title requires age 18 or older", status_code=status.HTTP_403_FORBIDDEN)
    return {
        "movie_id": movie_id,
        "user_id": user_id,
        "status": "playing"
    }


@app.get("/movies/{movie_id}/availability")
async def check_availability(movie_id: int, region: str):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    if region not in movie["regions"]:
        raise FilimoError(code="region_locked", message="this title is not available in region EU", status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
    return {
        "available": True,
        "movie_id": movie_id,
        "region": region,
    }


@app.post("/subscriptions")
async def create_subscription(payload: dict):
    user = find_user(payload["user_id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user["tier"] == payload["tier"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already on this tier")
    user["tier"] = payload["tier"]
    return JSONResponse(content={"user_id": payload["user_id"], "tier": payload["tier"]}, status_code=status.HTTP_201_CREATED)
