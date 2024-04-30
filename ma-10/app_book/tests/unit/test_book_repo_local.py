# /tests/unit/test_printing_repo.py

from uuid import uuid4, UUID

import pytest

from app.models.book import Book, BookStatus
from app.repositories.local_book_repo import BookRepo

book_test_repo = BookRepo()


def test_empty_list() -> None:
    assert book_test_repo.get_book() == []


def test_add_first_book() -> None:
    book = Book(id=UUID('41b5b60a-30d5-4b06-ba80-9ab409fde0ab'), title="Война и мир", status=BookStatus.CREATE,
                address='address_1', customer='customer_1')
    assert book_test_repo.create_book(book) == book


def test_add_first_book_repeat() -> None:
    book = Book(id=UUID('41b5b60a-30d5-4b06-ba80-9ab409fde0ab'), title="Война и мир", status=BookStatus.CREATE,
                address='address_1', customer='customer_1')
    with pytest.raises(KeyError):
        book_test_repo.create_book(book)


def test_get_book_by_id() -> None:
    book = Book(id=uuid4(), title="Война и мир", status=BookStatus.CREATE,
                address='address_1', customer='customer_1')
    book_test_repo.create_book(book)
    assert book_test_repo.get_book_by_id(book.id) == book


def test_get_book_by_id_error() -> None:
    with pytest.raises(KeyError):
        book_test_repo.get_book_by_id(uuid4())


def test_set_status() -> None:
    book = Book(id=uuid4(), title="Война и мир", status=BookStatus.CREATE,
                address='address_1', customer='customer_1')
    book_test_repo.create_book(book)

    book.status = BookStatus.CREATE
    assert book_test_repo.set_status(book).status == book.status

    book.status = BookStatus.PICK_UP
    assert book_test_repo.set_status(book).status == book.status

    book.status = BookStatus.DELIVERING
    assert book_test_repo.set_status(book).status == book.status

    book.status = BookStatus.DELIVERED
    assert book_test_repo.set_status(book).status == book.status

    book.status = BookStatus.PAID
    assert book_test_repo.set_status(book).status == book.status

    book.status = BookStatus.DONE
    assert book_test_repo.set_status(book).status == book.status
