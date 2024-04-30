from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import settings

engine_book = create_engine(settings.postgres_url_book, echo=True)
SessionLocalBook = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_book)


def get_db_book():
    db_book = SessionLocalBook()
    try:
        yield db_book
    finally:
        db_book.close()


# def get_db_document():
#     db_document = SessionLocalDoc()
#     try:
#         yield db_document
#     finally:
#         db_document.close()
