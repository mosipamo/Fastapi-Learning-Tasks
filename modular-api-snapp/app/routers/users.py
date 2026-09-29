from fastapi import APIRouter, HTTPException

from app.data import get_user, users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
async def list_users(role: str | None = None):
    if role:
        return [user for user in users if user["role"] == role]
    return users


@router.get("/{user_id}")
async def retrieve_user(user_id: int):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
