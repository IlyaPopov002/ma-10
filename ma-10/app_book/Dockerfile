FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_book

# Установка зависимостей проекта
COPY ./requirements.txt /app_book/
RUN pip install --no-cache-dir --upgrade -r /app_book/requirements.txt

# Перенос проекта в образ
COPY ./app /app_book/app
COPY .env /app_book

# Копирование файлов alembic
COPY ./migration /app_book/migration
COPY ./alembic.ini /app_book/alembic.ini

EXPOSE 80

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 80"]
# 80
