# /tests/integration/app_repositories/test_db_delivery_repo.py
from uuid import UUID, uuid4

import pytest

from app.models.book import Book, BookStatus
from app.repositories.db_book_repo import BookRepo


@pytest.fixture()
def book_repo() -> BookRepo:
    repo = BookRepo()
    return repo


@pytest.fixture(scope='session')
def book_id() -> UUID:
    return uuid4()


@pytest.fixture(scope='session')
def first_book() -> Book:
    return Book(id=UUID('f52220d4-01e6-47ac-83e3-4fb1c6bff697'), title="Война и мир", status=BookStatus.CREATE,
                address='address_1', customer='customer_1')


@pytest.fixture(scope='session')
def second_book() -> Book:
    return Book(id=UUID('876f608a-b400-480a-b661-df2d7e240747'), title="Преступление и наказание", status=BookStatus.CREATE,
                address='address_2', customer='customer_2')


def test_add_first_book(first_book: Book, book_repo: BookRepo) -> None:
    assert book_repo.create_book(first_book) == first_book


def test_add_first_book_repeat(first_book: Book, book_repo: BookRepo) -> None:
    with pytest.raises(KeyError):
        book_repo.create_book(first_book)


def test_get_book_by_id(first_book: Book, book_repo: BookRepo) -> None:
    assert book_repo.get_book_by_id(first_book.id) == first_book


def test_get_book_by_id_error(book_repo: BookRepo) -> None:
    with pytest.raises(KeyError):
        book_repo.get_book_by_id(uuid4())


def test_add_second_book(first_book: Book, second_book: Book, book_repo: BookRepo) -> None:
    assert book_repo.create_book(second_book) == second_book
    books = [book_repo.get_book_by_id(
        first_book.id), book_repo.get_book_by_id(second_book.id)]
    assert len(books) == 2
    assert books[0] == first_book
    assert books[1] == second_book


def test_set_status(first_book: Book, book_repo: BookRepo) -> None:
    first_book.status = BookStatus.ACCEPTED
    assert book_repo.set_status(first_book).status == first_book.status

    first_book.status = BookStatus.PICK_UP
    assert book_repo.set_status(first_book).status == first_book.status

    first_book.status = BookStatus.DELIVERING
    assert book_repo.set_status(first_book).status == first_book.status

    first_book.status = BookStatus.DELIVERED
    assert book_repo.set_status(first_book).status == first_book.status

    first_book.status = BookStatus.PAID
    assert book_repo.set_status(first_book).status == first_book.status

    first_book.status = BookStatus.DONE
    assert book_repo.set_status(first_book).status == first_book.status


def test_delete_created_book(first_book: Book, second_book: Book, book_repo: BookRepo) -> None:
    assert book_repo.delete_book_by_id(first_book.id) == first_book
    assert book_repo.delete_book_by_id(second_book.id) == second_book
