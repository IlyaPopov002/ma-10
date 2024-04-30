import datetime
from uuid import UUID

from app.models.document import Document
from typing import Optional

# documents: list[Document] = [
#     Document(id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), book_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
#              create_date=datetime.datetime.now(), doc='doc_1', customer='Andrey'),
#     Document(id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'), book_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
#              create_date=datetime.datetime.now(), doc='doc_2', customer='Ivan'),
#     Document(id=UUID('45309954-8e3c-4635-8066-b342f634252c'), book_id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
#              create_date=datetime.datetime.now(), doc='doc_2', customer='Pasha'),
# ]

documents = []


class DocumentRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            documents.clear()

    def get_document(self) -> list[Document]:
        return documents

    def get_document_by_id(self, id: UUID) -> Document:
        for d in documents:
            if d.id == id:
                return d

        raise KeyError

    def create_document(self, doc: Document) -> Document:
        if len([d for d in documents if d.id == doc.id]) > 0:
            raise KeyError

        documents.append(doc)
        return doc

    def delete_doc(self, id: UUID) -> Optional[Document]:
        for i, document in enumerate(documents):
            if document.id == id:
                deleted_document = documents.pop(i)
                return deleted_document

        return None
