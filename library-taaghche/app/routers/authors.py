from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..db import get_session
from ..models import Author, Book, AuthorCreate, AuthorUpdate, AuthorRead, AuthorList, AuthorWithBooks
from ..repository import list_authors

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("", response_model=AuthorRead, status_code=201)
def create_author(
    data: AuthorCreate,
    session: Session = Depends(get_session),
):
    author = Author.model_validate(data)

    session.add(author)
    session.commit()
    session.refresh(author)

    return author


@router.get("", response_model=AuthorList)
def get_authors(
    country: str | None = None,
    sort: str | None = None,
    page: int = 1,
    size: int = 10,
    session: Session = Depends(get_session),
):
    total, items = list_authors(
        session,
        country=country,
        sort=sort,
        page=page,
        size=size,
    )

    return {
        "total": total,
        "page": page,
        "size": size,
        "items": items,
    }


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(
    author_id: int,
    session: Session = Depends(get_session),
):
    author = session.get(Author, author_id)

    if not author or author.is_deleted:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@router.get("/{author_id}/books", response_model=AuthorWithBooks)
def get_author_books(
    author_id: int,
    session: Session = Depends(get_session),
):
    author = session.get(Author, author_id)

    if not author or author.is_deleted:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    statement = select(Book).where(
        Book.author_id == author_id,
        Book.is_deleted == False,
    )

    books = session.exec(statement).all()

    return {
        "id": author.id,
        "name": author.name,
        "country": author.country,
        "books": books,
    }


@router.patch("/{author_id}", response_model=AuthorRead)
def update_author(
    author_id: int,
    data: AuthorUpdate,
    session: Session = Depends(get_session),
):
    author = session.get(Author, author_id)

    if not author or author.is_deleted:
        raise HTTPException(status_code=404, detail="Author not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(author, key, value)

    session.add(author)
    session.commit()
    session.refresh(author)

    return author


@router.delete("/{author_id}", status_code=204)
def delete_author(
    author_id: int,
    session: Session = Depends(get_session),
):
    author = session.get(Author, author_id)

    if not author or author.is_deleted:
        raise HTTPException(status_code=404, detail="Author not found")

    author.is_deleted = True

    session.add(author)
    session.commit()

    return Response(status_code=204)


@router.post("/{author_id}/restore", response_model=AuthorRead)
def restore_author(
    author_id: int,
    session: Session = Depends(get_session),
):
    author = session.get(Author, author_id)

    if not author or not author.is_deleted:
        raise HTTPException(status_code=404, detail="Deleted author not found")

    author.is_deleted = False

    session.add(author)
    session.commit()
    session.refresh(author)

    return author
