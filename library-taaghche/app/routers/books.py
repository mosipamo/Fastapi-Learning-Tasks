from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..db import get_session
from ..models import Book, Author, BookCreate, BookUpdate, BookRead, BookList
from ..repository import list_books


router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookRead, status_code=201)
def create_book(
    data: BookCreate,
    session: Session = Depends(get_session),
):
    if data.author_id is not None:
        author = session.get(Author, data.author_id)

        if not author or author.is_deleted:
            raise HTTPException(
                status_code=404,
                detail="Author not found"
            )

        statement = select(Book).where(
            Book.title == data.title,
            Book.author_id == data.author_id,
            Book.is_deleted == False,
        )

        existing_book = session.exec(statement).first()

        if existing_book:
            raise HTTPException(
                status_code=409,
                detail="This author already has a book with this title"
            )

    book = Book.model_validate(data)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@router.get("", response_model=BookList)
def get_books(
    author_id: int | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    q: str | None = None,
    sort: str | None = None,
    page: int = 1,
    size: int = 10,
    session: Session = Depends(get_session),
):
    total, items = list_books(
        session,
        author_id=author_id,
        min_year=min_year,
        max_year=max_year,
        q=q,
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


@router.get("/{book_id}", response_model=BookRead)
def get_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    book = session.get(Book, book_id)

    if not book or book.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    data: BookUpdate,
    session: Session = Depends(get_session),
):
    book = session.get(Book, book_id)

    if not book or book.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = data.model_dump(exclude_unset=True)

    if "author_id" in update_data and update_data["author_id"] is not None:
        author = session.get(Author, update_data["author_id"])

        if not author or author.is_deleted:
            raise HTTPException(status_code=404, detail="Author not found")

    for key, value in update_data.items():
        setattr(book, key, value)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    book = session.get(Book, book_id)

    if not book or book.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    book.is_deleted = True

    session.add(book)
    session.commit()

    return Response(status_code=204)


@router.post("/{book_id}/restore", response_model=BookRead)
def restore_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    book = session.get(Book, book_id)

    if not book or not book.is_deleted:
        raise HTTPException(status_code=404, detail="Deleted book not found")

    book.is_deleted = False

    session.add(book)
    session.commit()
    session.refresh(book)

    return book
