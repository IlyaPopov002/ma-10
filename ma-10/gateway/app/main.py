from fastapi import FastAPI, Depends, Request, APIRouter
from starlette.middleware.sessions import SessionMiddleware
import httpx
from gateway.app.endpoints.auth_router import get_user_role
from gateway.app.endpoints.auth_router import auth_router
from starlette.responses import RedirectResponse
from uuid import UUID
from app_book.app.models.book import CreateBookRequest

host_ip = "localhost"
auth_url = "http://localhost:8000/auth/login"

# logging.basicConfig()

app = FastAPI(title='Service')

user_router = APIRouter(prefix='/user', tags=['user'])
staff_router = APIRouter(prefix='/staff', tags=['staff'])
app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')

MICROSERVICES = {
    "book": "http://localhost:80/api",
    "document": "http://localhost:81/api",
}


def proxy_request(service_name: str, path: str, user_info, request: Request, json_data: dict = None):
    url = f"{MICROSERVICES[service_name]}{path}"
    timeout = 20
    headers = {
        'user': str(user_info)
    }
    print(request.method)
    if request.method == 'GET':
        response = httpx.get(url, headers=headers, timeout=timeout).json()
    elif request.method == 'POST':
        response = httpx.post(url, headers=headers,
                              json=json_data, timeout=timeout).json()
    elif request.method == 'PUT':
        response = httpx.put(url, headers=headers, json=json_data).json()
    elif request.method == 'DELETE':
        response = httpx.delete(url, headers=headers).json()

    return response

# ___BOOK___


@staff_router.get("/book")
def read_book(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        print(
            f"\nrequest.session['prev_url'] = {request.session['prev_url']}\n")
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path="/book/", user_info=current_user, request=request)


@user_router.post("/book/add", response_model=CreateBookRequest)
def add_book(request: Request, book_request: CreateBookRequest, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path="/book/add", user_info=current_user, request=request, json_data=book_request.dict())


@staff_router.post("/book/add", response_model=CreateBookRequest)
def add_book(request: Request, book_request: CreateBookRequest, current_user: dict = Depends(get_user_role)):
    print(f"\n/book/add\n")
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path="/book/add", user_info=current_user, request=request, json_data=book_request.dict())


@user_router.get("/book/{id}")
def read_book_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}", user_info=current_user, request=request)


@staff_router.get("/book/{id}")
def read_book_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}", user_info=current_user, request=request)


@staff_router.post('/book/{id}/accepted')
def accepted_book(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}/accepted", user_info=current_user, request=request)


@staff_router.post('/book/{id}/pick_up')
def pick_up_book(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}/pick_up", user_info=current_user, request=request)


@staff_router.post('/book/{id}/delivering')
def delivering_book(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}/delivering", user_info=current_user, request=request)


@staff_router.post('/book/{id}/delivered')
def delivered_book(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}/delivered", user_info=current_user, request=request)


@staff_router.post('/book/{id}/paid')
def paid_book(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}/paid", user_info=current_user, request=request)


@staff_router.post('/book/{id}/done')
def done_book(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}/done", user_info=current_user, request=request)


@staff_router.post('/book/{id}/cancel')
def cancel_book(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}/cancel", user_info=current_user, request=request)


@staff_router.post('/book/{id}/delete')
def delete_book(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="book", path=f"/book/{id}/delete", user_info=current_user, request=request)

# ___DOCUMENT___


@staff_router.get("/document")
def read_document(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="document", path="/document/", user_info=current_user, request=request)


# @staff_router.get("/document/{id}")
# def read_book_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
#     if current_user['id'] == '':
#         request.session['prev_url'] = str(request.url)
#         return RedirectResponse(url=auth_url)
#     else:
#         return proxy_request(service_name="document", path=f"/document/{id}", user_info=current_user, request=request)


@user_router.get("/document/{id}")
def read_document_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="document", path=f"/document/{id}", user_info=current_user, request=request)


@staff_router.post('/document/{id}/delete')
def delete_dcoument(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="document", path=f"/document/{id}/delete", user_info=current_user, request=request)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(staff_router)
