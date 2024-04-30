from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.models.book import BookStatus
from app.schemas.base_schema import Base


class Book(Base):
    __tablename__ = 'book'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(Enum(BookStatus), nullable=False)
    address = Column(String, nullable=False)
    customer = Column(String, nullable=False)
