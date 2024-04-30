# 1. Поменять int на UUID в функциях

from uuid import UUID, uuid4
from fastapi import Depends
from datetime import datetime
import asyncio

from app.models.book import Book, BookStatus
from app.rabbitmq import send_to_document_queue
from app.repositories.db_book_repo import BookRepo


class BookService():
    book_repo: BookRepo

    def __init__(self, book_repo: BookRepo = Depends(BookRepo), ) -> None:
        self.book_repo = book_repo

    def get_book(self) -> list[Book]:
        return self.book_repo.get_book()

    def create_book(self, title: str, address: str, customer: str) -> Book:
        book = Book(id=uuid4(), title=title, status=BookStatus.CREATE,
                    address=address, customer=customer)
        return self.book_repo.create_book(book)

    def get_book_by_id(self, id: UUID) -> Book:
        return self.book_repo.get_book_by_id(id)

    def accepted_book(self, id: UUID) -> Book:
        book = self.book_repo.get_book_by_id(id)
        if book.status != BookStatus.CREATE:
            raise ValueError

        book.status = BookStatus.ACCEPTED

        book_data = {
            "id": uuid4(),
            "book_id": id,
            "create_date": datetime.now(),
            "doc": "Document",
            "customer": book.customer
        }

        asyncio.run(send_to_document_queue(book_data))

        return self.book_repo.set_status(book)

    def pick_up_book(self, id: UUID) -> Book:
        book = self.book_repo.get_book_by_id(id)
        if book.status != BookStatus.ACCEPTED:
            raise ValueError

        book.status = BookStatus.PICK_UP
        return self.book_repo.set_status(book)

    def delivering_book(self, id: UUID) -> Book:
        book = self.book_repo.get_book_by_id(id)
        if book.status != BookStatus.PICK_UP:
            raise ValueError

        book.status = BookStatus.DELIVERING
        return self.book_repo.set_status(book)

    def delivered_book(self, id: UUID) -> Book:
        book = self.book_repo.get_book_by_id(id)
        if book.status != BookStatus.DELIVERING:
            raise ValueError

        book.status = BookStatus.DELIVERED
        return self.book_repo.set_status(book)

    def paid_book(self, id: UUID) -> Book:
        book = self.book_repo.get_book_by_id(id)
        if book.status != (BookStatus.DELIVERED or BookStatus.DELIVERING):
            raise ValueError

        book.status = BookStatus.PAID
        return self.book_repo.set_status(book)

    def done_book(self, id: UUID) -> Book:
        book = self.book_repo.get_book_by_id(id)
        if book.status != BookStatus.PAID:
            raise ValueError

        book.status = BookStatus.DONE
        return self.book_repo.set_status(book)

    def cancel_book(self, id: UUID) -> Book:
        book = self.book_repo.get_book_by_id(id)
        if book.status != (BookStatus.CREATE or BookStatus.ACCEPTED):
            raise ValueError

        book.status = BookStatus.CANCELED
        return self.book_repo.set_status(book)

    def delete_book(self, id: UUID) -> None:
        book = self.book_repo.get_book_by_id(id)
        if not book:
            raise ValueError(f'book with id={id} not found')

        return self.book_repo.delete_book_by_id(id)
