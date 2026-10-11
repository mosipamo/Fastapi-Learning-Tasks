from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import User, UserCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Cafe Bazaar Accounts API", lifespan=lifespan)


@app.post("/users", status_code=201)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    try:
        db_user = User(
            username=user.username,
            email=user.email,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=409, detail=str(e))

@app.get("/users/{user_id}")
async def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users")
async def get_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    users = session.exec(select(User).order_by(User.id).offset(skip).limit(limit)).all()
    return users
