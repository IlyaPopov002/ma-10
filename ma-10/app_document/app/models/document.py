from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict, BaseModel


class Document(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    book_id: UUID
    customer: str
    create_date: datetime
    doc: str


class CreateDocumentRequest(BaseModel):
    book_id: UUID
    doc: str
    customer: str
