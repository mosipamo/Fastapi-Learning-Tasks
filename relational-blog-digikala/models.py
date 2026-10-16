from sqlmodel import Field, Relationship, SQLModel


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    posts: list["Post"] = Relationship(back_populates="author")


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int | None = Field(default=None, foreign_key="author.id")
    author: Author | None = Relationship(back_populates="posts")


class AuthorCreate(SQLModel):
    name: str


class PostCreate(SQLModel):
    title: str
    content: str
