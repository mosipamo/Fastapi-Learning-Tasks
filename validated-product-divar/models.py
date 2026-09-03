from pydantic import BaseModel, Field, field_validator

ALLOWED_CATEGORIES = {"real-estate", "vehicles", "electronics", "home", "services"}


class ProductIn(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    price: int = Field(gt=0, le=100_000_000_000)
    category: str = Field(...)
    city: str = Field(min_length=2, max_length=40)
    description: str | None = Field(max_length=500, default=None)
    seller_phone: str = Field(min_length=8, max_length=15)

    @field_validator("category")
    def validate_category(cls, value) -> str:
        if value.lower() not in ALLOWED_CATEGORIES:
            raise ValueError(f"Invalid category: {value}")
        return value.lower()

    @field_validator("title")
    def validate_title(cls, value) -> str:
        if value.strip() is "":
            raise ValueError("Title cannot be empty")
        return value.strip()

class ProductOut(BaseModel):
    id: int
    title: str
    price: int
    category: str
    city: str
    description: str | None
