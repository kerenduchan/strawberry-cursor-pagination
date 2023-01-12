import base64
import typing


class DBBook:
    id: int
    title: str

    def __init__(self, id_: int, title: str):
        self.id = id_
        self.title = title


def encode(val: str) -> str:
    val_bytes = base64.b64encode(val.encode('ascii'))
    return val_bytes.decode('ascii')


def decode(val: str) -> str:
    val_bytes = base64.b64decode(val.encode('ascii'))
    return val_bytes.decode('ascii')


BOOKS_COUNT = 20

# The mock DB, ordered by title.
books = [DBBook(id_=i, title=f'Title {i}')
         for i in range(1, BOOKS_COUNT + 1)]


def build_book_cursor(book):
    """
    The book cursor must be based on the same "db column" that the result of
    get_books is ordered by.
    """
    return encode(book.title)


def get_books(limit: int, cursor: typing.Optional[str]) -> typing.List[DBBook]:
    """
    Return first given number books, starting after the given cursor,
    ordered by title. Cursor must be an encoded title, or None in order
    to start at the beginning.
    """
    if cursor is None:
        # start at the beginning
        return books[:limit]

    start_title = decode(cursor)
    found_idx = [idx for idx, book in enumerate(books)
                 if book.title == start_title]
    if len(found_idx) == 0:
        # cursor not found
        raise Exception(f'Cursor not found: {cursor}')

    start_idx = found_idx[0] + 1
    end_idx = start_idx + limit
    return books[start_idx:end_idx]
