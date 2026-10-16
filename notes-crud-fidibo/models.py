from sqlmodel import SQLModel, Field


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=2000)
    tag: str | None = Field(max_length=30, default=None)


class NoteCreate(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=2000)
    tag: str | None = Field(max_length=30, default=None)


class NoteUpdate(SQLModel):
    title: str | None = Field(min_length=1, max_length=100, default=None)
    content: str | None = Field(max_length=2000, default=None)
    tag: str | None = Field(max_length=30, default=None)
