import enum
from uuid import UUID
from pydantic import ConfigDict, BaseModel
from typing import Optional


class BookStatus(enum.Enum):
    CREATE = 'create'
    ACCEPTED = 'accepted'
    PICK_UP = 'pick_up'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    PAID = 'paid'
    DONE = 'done'
    CANCELED = 'canceled'


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    status: BookStatus
    address: str
    customer: str


class CreateBookRequest(BaseModel):
    title: str
    address: str
    customer: str
