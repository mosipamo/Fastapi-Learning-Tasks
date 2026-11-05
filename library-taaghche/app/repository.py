from app.models import Author, Book

from sqlmodel import Session, select, col, func, asc, desc


def list_books(
    session: Session,
    *,
    author_id: int | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    q: str | None = None,
    sort: str | None = None,
    page: int = 1,
    size: int = 10,
) -> tuple[int, list[Book]]:

    statement = select(Book).where(Book.is_deleted == False)

    if author_id is not None:
        statement = statement.where(Book.author_id == author_id)

    if min_year is not None:
        statement = statement.where(Book.year >= min_year)

    if max_year is not None:
        statement = statement.where(Book.year <= max_year)

    if q:
        pattern = f"%{q}%"
        statement = statement.where(col(Book.title).ilike(pattern))

    count_statement = select(func.count()).select_from(Book).where(
        Book.is_deleted == False
    )

    if author_id is not None:
        count_statement = count_statement.where(Book.author_id == author_id)

    if min_year is not None:
        count_statement = count_statement.where(Book.year >= min_year)

    if max_year is not None:
        count_statement = count_statement.where(Book.year <= max_year)

    if q:
        pattern = f"%{q}%"
        count_statement = count_statement.where(col(Book.title).ilike(pattern))

    total = session.exec(count_statement).one()

    if sort:
        descending = sort.startswith("-")
        field = sort[1:] if descending else sort

        sort_columns = {
            "title": Book.title,
            "year": Book.year,
            "price": Book.price,
        }

        if field not in sort_columns:
            raise ValueError("Invalid sort field")

        column = sort_columns[field]

        statement = statement.order_by(
            desc(column) if descending else asc(column)
        )

    offset = (page - 1) * size

    statement = statement.offset(offset).limit(size)

    items = session.exec(statement).all()

    return total, items


def list_authors(
    session: Session,
    *,
    country: str | None = None,
    sort: str | None = None,
    page: int = 1,
    size: int = 10,
) -> tuple[int, list[Author]]:

    statement = select(Author).where(Author.is_deleted == False)

    if country is not None:
        statement = statement.where(Author.country == country)

    count_statement = select(func.count()).select_from(Author).where(
        Author.is_deleted == False
    )

    if country is not None:
        count_statement = count_statement.where(Author.country == country)

    total = session.exec(count_statement).one()

    if sort:
        descending = sort.startswith("-")
        field = sort[1:] if descending else sort

        sort_columns = {
            "name": Author.name,
            "country": Author.country,
        }

        if field not in sort_columns:
            raise ValueError("Invalid sort field")

        column = sort_columns[field]

        statement = statement.order_by(
            desc(column) if descending else asc(column)
        )

    offset = (page - 1) * size

    statement = statement.offset(offset).limit(size)

    items = session.exec(statement).all()

    return total, items
