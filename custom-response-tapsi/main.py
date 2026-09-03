from fastapi import FastAPI, HTTPException, Response, status
from data import find_ride, next_ride_id, rides
from rides import build_ride, next_status, ride_headers, validate_new_ride

app = FastAPI(title="Tapsi Ride Service")


@app.get("/")
def welcome():
    return {"message": "Tapsi ride service", "rides_count": len(rides)}


@app.post("/rides", status_code=status.HTTP_201_CREATED)
def create_ride(payload: dict, response: Response):
    error = validate_new_ride(payload)
    if error is not None:
        raise HTTPException(status_code=422, detail=error)

    new_id = next_ride_id()
    ride = build_ride(new_id, payload["origin"], payload["destination"], payload["price"])

    rides.append(ride)

    response.headers["Location"] = f"/rides/{new_id}"
    response.headers["X-Ride-Id"] = str(new_id)

    return ride


@app.get("/rides")
def list_rides(response: Response):
    response.headers["X-Total-Count"] = str(len(rides))
    return {"rides": rides}


@app.get("/rides/{ride_id}")
def get_ride(ride_id: int):
    ride = find_ride(ride_id)
    if ride is None:
        raise HTTPException(status_code=404, detail="ride not found")
    return ride


@app.patch("/rides/{ride_id}/status")
def advance_ride_status(ride_id: int, payload: dict):
    ride = find_ride(ride_id)
    if ride is None:
        raise HTTPException(status_code=404, detail="ride not found")

    requested = payload.get("status")
    expected = next_status(ride["status"])

    if expected is None or requested != expected:
        raise HTTPException(status_code=409, detail="invalid status transition")

    ride["status"] = expected
    return ride


@app.delete("/rides/{ride_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_ride(ride_id: int):
    ride = find_ride(ride_id)
    if ride is None:
        raise HTTPException(status_code=404, detail="ride not found")

    rides.remove(ride)
    return


@app.get("/session")
def start_session(response: Response):
    response.set_cookie(
        key="device_id",
        value="tapsi-device",
        max_age=3600,
        path="/",
        samesite="lax"
    )
    return {"message": "session started"}
