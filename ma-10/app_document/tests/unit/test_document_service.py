from uuid import uuid4, UUID

import pytest

from app.repositories.local_document_repo import DocumentRepo
from app.services.document_service import DocumentService


@pytest.fixture(scope='session')
def document_service() -> DocumentService:
    return DocumentService(DocumentRepo(clear=True))


# @pytest.fixture(scope='session')
# def first_document_data() -> tuple[UUID, str, str, str]:
#     return (uuid4(), 'test_document_type_1', 'test_document_doc_1', 'test_document_customer_info_1')

@pytest.fixture(scope='session')
def first_document_data() -> tuple[UUID, str, str]:
    return (uuid4(), 'customer_1', 'document_1',)


# @pytest.fixture(scope='session')
# def second_document_data() -> tuple[UUID, str, str, str]:
#     return (uuid4(), 'test_document_type_2', 'test_document_doc_2', 'test_document_customer_info_2')
@pytest.fixture(scope='session')
def second_document_data() -> tuple[UUID, str, str]:
    return (uuid4(), 'customer_2', 'document_2',)


def test_empty_document(document_service: DocumentService) -> None:
    assert document_service.get_document() == []


# def test_create_first_document(
#         first_document_data: tuple[UUID, str, str, str],
#         document_service: DocumentService
# ) -> None:
#     ord_id, type, doc, customer_info = first_document_data
#     document = document_service.create_document(
#         ord_id, type, doc, customer_info)
#     assert document.ord_id == ord_id
#     assert document.type == type
#     assert document.customer_info == customer_info
#     assert document.doc == doc
def test_create_first_document(
        first_document_data: tuple[UUID, str, str],
        document_service: DocumentService
) -> None:
    book_id, doc, customer = first_document_data
    document = document_service.create_document(
        book_id, doc, customer)
    assert document.book_id == book_id
    assert document.customer == customer
    assert document.doc == doc


# def test_create_second_document(
#         second_document_data: tuple[UUID, str, str, str],
#         document_service: DocumentService
# ) -> None:
#     ord_id, type, doc, customer_info = second_document_data
#     document = document_service.create_document(
#         ord_id, type, doc, customer_info)
#     assert document.ord_id == ord_id
#     assert document.type == type
#     assert document.customer_info == customer_info
#     assert document.doc == doc


def test_create_second_document(
        second_document_data: tuple[UUID, str, str],
        document_service: DocumentService
) -> None:
    book_id, doc, customer = second_document_data
    document = document_service.create_document(
        book_id, doc, customer)
    assert document.book_id == book_id
    assert document.customer == customer
    assert document.doc == doc


# def test_get_document_full(
#         first_document_data: tuple[UUID, str, str, str],
#         second_document_data: tuple[UUID, str, str, str],
#         document_service: DocumentService
# ) -> None:
#     documents = document_service.get_document()
#     assert len(documents) == 2
#     assert documents[0].ord_id == first_document_data[0]
#     assert documents[0].type == first_document_data[1]
#     assert documents[0].doc == first_document_data[2]
#     assert documents[0].customer_info == first_document_data[3]

#     assert documents[1].ord_id == second_document_data[0]
#     assert documents[1].type == second_document_data[1]
#     assert documents[1].doc == second_document_data[2]
#     assert documents[1].customer_info == second_document_data[3]

def test_get_document_full(
        first_document_data: tuple[UUID, str, str],
        second_document_data: tuple[UUID, str, str],
        document_service: DocumentService
) -> None:
    documents = document_service.get_document()
    assert len(documents) == 2
    assert documents[0].book_id == first_document_data[0]
    assert documents[0].doc == first_document_data[1]
    assert documents[0].customer == first_document_data[2]

    assert documents[1].book_id == second_document_data[0]
    assert documents[1].doc == second_document_data[1]
    assert documents[1].customer == second_document_data[2]
