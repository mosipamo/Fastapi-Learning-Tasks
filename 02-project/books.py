from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book():
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra":
        {
            "example":
            {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": "2010"
            }
        }
    }

class BookUpdate(BaseModel):
    id: int
    title: Optional[str] = Field(default=None, min_length=3)
    author: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1, max_length=100)
    rating: Optional[int] = Field(default=None, gt=0, lt=6)
    published_date: Optional[int] = None

    model_config = {
        "json_schema_extra":
        {
            "example":
            {
                "id": "1",
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": "2010"
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]
        

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)): 
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    result = []
    for book in BOOKS:
        if book.rating == book_rating:
            result.append(book)
    return result

@app.get("/books/getbypublishday/", status_code=status.HTTP_200_OK)
async def get_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    result = []
    for book in BOOKS:
        if book.published_date == published_date:
            result.append(book)
    return result


@app.post("/create-book/", status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookRequest):
    new_book = Book(**new_book.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update-book/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(updated_book: BookUpdate):
    found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == updated_book.id:
            found = True
            if updated_book.title is not None:
                BOOKS[i].title = updated_book.title
            if updated_book.author is not None:
                BOOKS[i].author = updated_book.author
            if updated_book.description is not None:
                BOOKS[i].description = updated_book.description
            if updated_book.rating is not None:
                BOOKS[i].rating = updated_book.rating
            if updated_book.published_date is not None:
                BOOKS[i].published_date = updated_book.published_date
            break

    if not found:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/delete-book/", status_code=status.HTTP_204_NO_CONTENT )
async def delete_book(book_id: int):
    flag = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            flag = True
            BOOKS.pop(i)
            break
    if not flag:
        raise HTTPException(status_code=404, detail="Item not found")


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1] + 1
    return book

