from fastapi import APIRouter, HTTPException

from app.data import get_ride, rides

router = APIRouter(prefix="/rides", tags=["rides"])


@router.get("")
async def get_rides(status: str | None = None):
    if status:
        return [ride for ride in rides if ride["status"] == status]
    return rides


@router.get("/{ride_id}")
async def get_ride_by_id(ride_id: int):
    ride = get_ride(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride
