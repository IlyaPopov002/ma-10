from fastapi import Request
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry import trace
import asyncio
import prometheus_client
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi import APIRouter, Depends, HTTPException, Response
import json
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.services.book_service import BookService
from app.models.book import Book, CreateBookRequest

book_router = APIRouter(prefix='/book', tags=['Book'])


# @book_router.get('/')
# def get_book(book_service: BookService = Depends(BookService)) -> list[Book]:
#     print('\n///get_book///\n')
#     return book_service.get_book()


# @book_router.post('/')
# def create_book(
#         book: CreateBookRequest,
#         book_service: BookService = Depends(BookService)
# ) -> Book:
#     try:
#         print('\n///post_book///\n')
#         book = book_service.create_book(book.address, book.customer,
#                                         book.title)
#         return book.dict()
#     except KeyError:
#         raise HTTPException(
#             400, f'Book with id={book.id} already exists')


# @book_router.post('/{id}/accepted')
# def accepted_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
#     try:
#         book = book_service.accepted_book(id)
#         return book.dict()
#     except KeyError:
#         raise HTTPException(404, f'Book with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Book with id={id} can\'t be activated')


# @book_router.post('/{id}/pick_up')
# def pick_up_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
#     try:
#         book = book_service.pick_up_book(id)
#         return book.dict()
#     except KeyError:
#         raise HTTPException(404, f'Book with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Book with id={id} can\'t be pick_up')


# @book_router.post('/{id}/delivering')
# def delivering_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
#     try:
#         book = book_service.delivering_book(id)
#         return book.dict()
#     except KeyError:
#         raise HTTPException(404, f'Book with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Book with id={id} can\'t be delivering')


# @book_router.post('/{id}/delivered')
# def delivered_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
#     try:
#         book = book_service.delivered_book(id)
#         return book.dict()
#     except KeyError:
#         raise HTTPException(404, f'Book with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Book with id={id} can\'t be delivered')


# @book_router.post('/{id}/paid')
# def paid_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
#     try:
#         book = book_service.paid_book(id)
#         return book.dict()
#     except KeyError:
#         raise HTTPException(404, f'Book with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Book with id={id} can\'t be paid')


# @book_router.post('/{id}/done')
# def done_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
#     try:
#         book = book_service.done_book(id)
#         return book.dict()
#     except KeyError:
#         raise HTTPException(404, f'Book with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Book with id={id} can\'t be done')


# @book_router.post('/{id}/canceled')
# def cancel_delivery(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
#     try:
#         book = book_service.cancel_book(id)
#         return book.dict()
#     except KeyError:
#         raise HTTPException(404, f'Book with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Book with id={id} can\'t be canceled')


# @book_router.post('/{id}/delete')
# def delete_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
#     try:
#         book = book_service.delete_book(id)
#         return book.dict()
#     except KeyError:
#         raise HTTPException(404, f'Book with id={id} not found')


# book_router = APIRouter(prefix='/book', tags=['Book'])

book_router = APIRouter(prefix='/book', tags=['Book'])


provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "book-delivery"})
    )
)
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

name = 'Book Delivery'
tracer = trace.get_tracer(name)


delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])
metrics_router = APIRouter(tags=['Metrics'])

get_deliveries_count = prometheus_client.Counter(
    "get_book_deliveries_count",
    "Total got all book deliveries"
)

created_delivery_count = prometheus_client.Counter(
    "created_book_delivery_count",
    "Total created book deliveries"
)

started_delivery_count = prometheus_client.Counter(
    "started_printing_count",
    "Total started book deliveries"
)

completed_delivery_count = prometheus_client.Counter(
    "completed_printing_count",
    "Total completed book deliveries"
)

cancelled_delivery_count = prometheus_client.Counter(
    "cancelled_printing_count",
    "Total canceled book deliveries"
)


def user_admin(role):
    if role == "service_user" or role == "service_admin":
        return True
    return False


def admin(role):
    if role == "service_admin":
        return True
    return False


@book_router.get('/')
def get_book(book_service: BookService = Depends(BookService), user: str = Header(...)) -> list[Book]:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    return book_service.get_book()
                raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')


@book_router.post('/add')
async def add_book(request: Request, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        request_body = await request.body()
        request_data = json.loads(request_body)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if user_admin(user['role']):
                    get_deliveries_count.inc(1)
                    book = book_service.create_book(request_data.get(
                        "title"), request_data.get("address"), request_data.get("customer"))
                    return book.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(400, f'Book with id= already exists')


@book_router.get('/{id}')
def get_book_by_id(id: UUID, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if user_admin(user['role']):
                    get_deliveries_count.inc(1)
                    return book_service.get_book_by_id(id)
                raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')


@book_router.post('/{id}/accepted')
def accepted_book(id: UUID, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    book = book_service.accepted_book(id)
                    return book.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be activated')


@book_router.post('/{id}/pick_up')
def pick_up_book(id: UUID, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    book = book_service.pick_up_book(id)
                    return book.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be activated')


@book_router.post('/{id}/delivering')
def delivering_book(id: UUID, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    book = book_service.delivering_book(id)
                    return book.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be activated')


@book_router.post('/{id}/delivered')
def delivered_book(id: UUID, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    book = book_service.delivered_book(id)
                    return book.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be activated')


@book_router.post('/{id}/paid')
def paid_book(id: UUID, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    book = book_service.paid_book(id)
                    return book.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be activated')


@book_router.post('/{id}/done')
def done_book(id: UUID, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    book = book_service.done_book(id)
                    return book.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be activated')


@book_router.post('/{id}/cancel')
def cancel_book(id: UUID, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if user_admin(user['role']):
                    get_deliveries_count.inc(1)
                    book = book_service.cancel_book(id)
                    return book.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be activated')


@book_router.post('/{id}/delete')
def delete_book(id: UUID, book_service: BookService = Depends(BookService), user: str = Header(...)) -> Book:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get book deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    book = book_service.delete_book(id)
                    return book.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be activated')


@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )
