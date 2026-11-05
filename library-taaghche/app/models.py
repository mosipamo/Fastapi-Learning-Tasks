from sqlmodel import Field, SQLModel, Relationship



class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1)
    country: str = Field(min_length=2)
    is_deleted: bool = False

    books: list["Book"] = Relationship(back_populates="author")


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1)
    year: int = Field(gt=1000, le=2100)
    price: int = Field(gt=0)
    author_id: int = Field(foreign_key="author.id")
    is_deleted: bool = False

    author: "Author" = Relationship(back_populates="books")


class AuthorCreate(SQLModel):
    name: str = Field(min_length=1)
    country: str = Field(min_length=2)


class AuthorUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1)
    country: str | None = Field(default=None, min_length=2)


class AuthorRead(SQLModel):
    id: int
    name: str
    country: str


class BookCreate(SQLModel):
    title: str = Field(min_length=1)
    year: int = Field(ge=1000, le=2100)
    price: int = Field(gt=0)
    author_id: int | None = None


class BookUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1)
    year: int | None = Field(default=None, ge=1000, le=2100)
    price: int | None = Field(default=None, gt=0)
    author_id: int | None = None


class BookRead(SQLModel):
    id: int
    title: str
    year: int
    price: int
    author_id: int | None


class AuthorWithBooks(AuthorRead):
    books: list[BookRead]


class AuthorList(SQLModel):
    total: int
    page: int
    size: int
    items: list[AuthorRead]


class BookList(SQLModel):
    total: int
    page: int
    size: int
    items: list[BookRead]
