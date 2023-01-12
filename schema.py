import strawberry
import db
from typing import List, Generic, TypeVar, Optional

GenericType = TypeVar("GenericType")


@strawberry.type
class Connection(Generic[GenericType]):
    """Represents a paginated relationship between two entities

    This pattern is used when the relationship itself has attributes.
    In a Facebook-based domain example, a friendship between two people
    would be a connection that might have a `friendshipStartTime`
    """
    page_info: "PageInfo"
    edges: List["Edge[GenericType]"]


@strawberry.type
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination

    Instead of classic offset pagination via `page` and `limit` parameters,
    here we have a cursor of the last object and we fetch items starting from that one

    Read more at:
        - https://graphql.org/learn/pagination/#pagination-and-edges
        - https://relay.dev/graphql/connections.htm
    """
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]


@strawberry.type
class Edge(Generic[GenericType]):
    """An edge may contain additional information of the relationship. This is the trivial case"""
    node: GenericType
    cursor: str


@strawberry.type
class Book:
    id: strawberry.ID
    title: str

    @classmethod
    def from_db_model(cls, instance: db.DBBook):
        """Adapt this method with logic to map your orm instance to a strawberry decorated class"""
        return cls(id=instance.id, title=instance.title)


Cursor = str


def get_books(first: int, after: Optional[Cursor]) -> Connection[Book]:
    # get one extra book to check whether there is a next page
    books = db.get_books(first + 1, after)

    edges = [
        Edge(node=Book.from_db_model(book), cursor=db.build_book_cursor(book))
        for book in books[:first]
    ]

    return Connection(
        page_info=PageInfo(
            has_previous_page=after is not None,
            has_next_page=len(books) > first,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if edges else None,
        ),
        edges=edges
    )


@strawberry.type
class Query:
    books: Connection[Book] = strawberry.field(resolver=get_books)


schema = strawberry.Schema(query=Query)
