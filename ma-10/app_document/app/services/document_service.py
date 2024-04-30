# 1. Поменять int на UUID в функциях

from uuid import UUID, uuid4
from fastapi import Depends
from datetime import datetime
from app.models.document import Document
from app.repositories.db_document_repo import DocumentRepo


class DocumentService():
    document_repo: DocumentRepo

    def __init__(self, document_repo: DocumentRepo = Depends(DocumentRepo)) -> None:
        self.document_repo = document_repo

    def get_document(self) -> list[Document]:
        return self.document_repo.get_document()

    def get_document_by_id(self, id: UUID) -> Document:
        return self.document_repo.get_document_by_id(id)

    def create_document(self, book_id: UUID, doc: str, customer: str) -> Document:
        document = Document(id=uuid4(), book_id=book_id, create_date=datetime.now(),
                            doc=doc, customer=customer)

        return self.document_repo.create_document(document)

    def delete_document(self, id: UUID) -> None:
        return self.document_repo.delete_document_by_id(id)
