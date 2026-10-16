from typing import Literal, Annotated
from contextlib import asynccontextmanager


from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select, col, or_

from db import create_db_and_tables, get_session
from models import Note, NoteCreate, NoteUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Fidibo Notes", lifespan=lifespan)

@app.post("/notes", status_code=201)
def create_note(payload: NoteCreate, session: Session = Depends(get_session)):
    if not payload.title or not payload.content:
        raise HTTPException(status_code=422, detail="Title and content are required")
    note = Note(title=payload.title, content=payload.content, tag=payload.tag)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.get("/notes/{note_id}")
def read_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.get("/notes")
def read_notes(
    session: Session = Depends(get_session),
    q: str = "",
    tag: str = "",
    sort: Annotated[Literal["id", "-id", "title"], Query()] = "id"
):
    pattern = f"%{q}%"
    statement = select(Note).where(
        or_(col(Note.title).ilike(pattern), col(Note.content).ilike(pattern))
    )

    if tag:
        statement = statement.where(col(Note.tag) == tag)

    if sort == "-id":
        statement = statement.order_by(col(Note.id).desc())
    elif sort == "title":
        statement = statement.order_by(col(Note.title))
    else:
        statement = statement.order_by(col(Note.id))

    notes = session.exec(statement).all()
    return notes


@app.put("/notes/{note_id}", status_code=200)
def update_note(note_id: int, payload: NoteUpdate, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    if not payload.title or not payload.content:
        raise HTTPException(status_code=400, detail="Title and content are required")

    note.title = payload.title
    note.content = payload.content
    note.tag = payload.tag
    session.commit()
    session.refresh(note)
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
