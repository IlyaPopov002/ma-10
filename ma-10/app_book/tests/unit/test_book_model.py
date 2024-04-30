# /tests/unit/test_printing_model.py

from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.models.book import Book, BookStatus


def test_book_creation():
    id = uuid4()
    title = "Война и мир"
    status = BookStatus.CREATE
    address = "address_1"
    customer = "customer_1"

    book = Book(id=id, title=title, status=status,
                address=address, customer=customer)

    assert dict(book) == {'id': id, 'title': title, 'status': status, 'address': address,
                          'customer': customer}


def test_book_title_required():
    with pytest.raises(ValidationError):
        Book(id=uuid4(), status=BookStatus.CREATE,
             address="address_1", customer="customer_1")


def test_book_status_required():
    with pytest.raises(ValidationError):
        Book(id=uuid4(), title="Война и мир",
             address="address_1", customer="customer_1")
