FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_document

# Установка зависимостей проекта
COPY ./requirements.txt /app_document/
RUN pip install --no-cache-dir --upgrade -r /app_document/requirements.txt

# Перенос проекта в образ
COPY ./app /app_document/app
COPY .env /app_document

# Копирование файлов alembic
COPY ./migration /app_document/migration
COPY ./alembic.ini /app_document/alembic.ini


# Добавляем путь к корневому каталогу проекта в PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app_document"
ENV PYTHONPATH="${PYTHONPATH}:/app_document/app"

# EXPOSE 81
# EXPOSE 8080

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 81"]
# 81