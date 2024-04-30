import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db_book
from app.models.book import Book
from app.schemas.book import Book as DBBook


class BookRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db_book())

    def _map_to_model(self, book: DBBook) -> Book:
        result = Book.from_orm(book)

        return result

    def _map_to_schema(self, book: Book) -> DBBook:
        data = dict(book)
        result = DBBook(**data)

        return result

    def get_book(self) -> list[Book]:
        books = []
        for d in self.db.query(DBBook).all():
            books.append(self._map_to_model(d))

        return books

    def get_book_by_id(self, id: UUID) -> Book:
        book = self.db \
            .query(DBBook) \
            .filter(DBBook.id == id) \
            .first()

        if book == None:
            raise KeyError
        return self._map_to_model(book)

    def create_book(self, book: Book) -> Book:
        try:
            db_book = self._map_to_schema(book)
            self.db.add(db_book)
            self.db.commit()
            return self._map_to_model(db_book)
        except:
            traceback.print_exc()
            raise KeyError

    def set_status(self, book: Book) -> Book:
        db_book = self.db.query(DBBook).filter(
            DBBook.id == book.id).first()
        db_book.status = book.status
        self.db.commit()
        return self._map_to_model(db_book)

    def delete_book_by_id(self, id: UUID) -> Book:
        try:
            # Find the Book by its id
            book = self.db.query(DBBook).filter(DBBook.id == id).one()

            # If the Book is found, map it to the model and commit the deletion
            if book:
                deleted_book = self._map_to_model(book)
                self.db.delete(book)
                self.db.commit()
                return deleted_book
            else:
                # Handle the case where no Book is found
                raise ValueError(f"No Book found with id {id}")
        except Exception as e:
            # Rollback any changes if there's an error
            self.db.rollback()
            # Re-raise the exception so it can be handled elsewhere
            raise e
