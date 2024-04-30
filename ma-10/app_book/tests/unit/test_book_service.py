from uuid import uuid4

import pytest

from app.models.book import BookStatus
from app.repositories.local_book_repo import BookRepo
from app.services.book_service import BookService


@pytest.fixture(scope='session')
def book_service() -> BookService:
    return BookService(BookRepo(clear=True))


@pytest.fixture(scope='session')
def first_book_data() -> tuple[str, str, str]:
    return ('Война и мир', 'adress_1', 'customer_1')


@pytest.fixture(scope='session')
def second_book_data() -> tuple[str, str, str]:
    return ('Преступление и наказание', 'adress_2', 'customer_2')


def test_empty_books(book_service: BookService) -> None:
    assert book_service.get_book() == []


def test_create_first_book(
        first_book_data: tuple[str, str, str],
        book_service: BookService
) -> None:
    title, address, customer = first_book_data
    book = book_service.create_book(title, address, customer)
    assert book.title == title
    assert book.address == address
    assert book.customer == customer


def test_create_second_book(
        second_book_data: tuple[str, str, str],
        book_service: BookService
) -> None:
    title, address, customer = second_book_data
    book = book_service.create_book(title, address, customer)
    assert book.title == title
    assert book.address == address
    assert book.customer == customer


def test_get_book_full(
        first_book_data: tuple[str, str, str],
        second_book_data: tuple[str, str, str],
        book_service: BookService
) -> None:
    books = book_service.get_book()
    assert len(books) == 2
    assert books[0].address == first_book_data[1]
    assert books[1].address == second_book_data[1]


def test_done_book_status_error(
        book_service: BookService
) -> None:
    with pytest.raises(ValueError):
        books = book_service.get_book()
        book_service.done_book(books[0].id)


def test_done_book_not_found(
        book_service: BookService
) -> None:
    with pytest.raises(KeyError):
        book_service.done_book(uuid4())


def test_accepted_book_not_found(
        book_service: BookService
) -> None:
    with pytest.raises(KeyError):
        book_service.accepted_book(uuid4())


def test_accepted_book(
        book_service: BookService
) -> None:
    book = book_service.get_book()[0]
    book_service.accepted_book(book.id)
    assert book.status == BookStatus.ACCEPTED
    assert book.id == book_service.get_book()[0].id


def test_done_book(
        book_service: BookService
) -> None:
    book = book_service.get_book()[0]
    book.status = BookStatus.PAID
    book_service.done_book(book.id)
    assert book.status == BookStatus.DONE
    assert book.id == book_service.get_book()[0].id
