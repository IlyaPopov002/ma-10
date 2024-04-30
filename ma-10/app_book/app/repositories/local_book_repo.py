from uuid import UUID
from app.models.book import Book
from typing import Optional

# books: list[Book] = [
#     Book(id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), status=BookStatus.CREATE, address='address_0', customer='Andrey',
#          create_date=datetime.datetime.now(), completion_date=datetime.datetime.now(), title='Преступление и наказание'),
#     Book(id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'), status=BookStatus.CREATE, address='address_1', customer='Ivan',
#          create_date=datetime.datetime.now(), completion_date=datetime.datetime.now(), title='Война и мир'),
#     Book(id=UUID('45309954-8e3c-4635-8066-b342f634252c'), status=BookStatus.CREATE, address='address_2', customer='Pasha',
#          create_date=datetime.datetime.now(), completion_date=datetime.datetime.now(), title='Евгений Онегин'),
# ]

books = []


class BookRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            books.clear()

    def get_book(self) -> list[Book]:
        return books

    def get_book_by_id(self, id: UUID) -> Book:
        for d in books:
            if d.id == id:
                return d

        raise KeyError

    def create_book(self, book: Book) -> Book:
        if len([d for d in books if d.id == book.id]) > 0:
            raise KeyError

        books.append(book)
        return book

    def set_status(self, book: Book) -> Book:
        for d in books:
            if d.id == book.id:
                d.status = book.status
                break

        return book

    def delete_book(self, id: UUID) -> Optional[Book]:
        for i, book in enumerate(books):
            if book.id == id:
                deleted_book = books.pop(i)
                return deleted_book

        return None
