from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.base_schema import Base


class Document(Base):
    __tablename__ = 'document'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    book_id = Column(UUID(as_uuid=True), nullable=False)
    customer = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    doc = Column(String, nullable=False)
