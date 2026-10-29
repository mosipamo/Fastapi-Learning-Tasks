from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    category: str = Field(index=True)
    price: int


class ProductRead(SQLModel):
    id: int
    title: str
    category: str
    price: int


class ProductPage(SQLModel):
    items: list[ProductRead]
    total: int
    page: int
    size: int
