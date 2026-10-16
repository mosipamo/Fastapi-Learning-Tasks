from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Author, AuthorCreate, Post, PostCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Digikala Mag API", lifespan=lifespan)


@app.post("/authors", status_code=201)
def create_author(author: AuthorCreate, session: Session = Depends(get_session)) -> Author:
    db_author = Author(name=author.name)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@app.post("/authors/{author_id}/posts", status_code=201)
def create_post(author_id: int, payload: PostCreate, session: Session = Depends(get_session)) -> Post:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db_post = Post(
        title=payload.title,
        content=payload.content,
        author_id=author_id
    )
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return {
        "id": db_post.id,
        "title": db_post.title,
        "content": db_post.content,
        "author_id": db_post.author_id,
    }


@app.get("/authors/{author_id}")
def read_author(author_id: int, session: Session = Depends(get_session)) -> dict:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return {
        "id": author.id,
        "name": author.name,
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author_id": post.author_id,
            }
            for post in author.posts
        ],
    }


@app.get("/posts")
def list_posts(author_id: int | None = None, session: Session = Depends(get_session)) -> list[Post]:
    if not author_id:
        posts = session.execute(select(Post).order_by(Post.id))
    else:
        posts = session.execute(select(Post).where(
            Post.author_id == author_id).order_by(Post.id))
    return [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
        }
        for post in posts
    ]
