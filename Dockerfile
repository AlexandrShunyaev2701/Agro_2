FROM python:3.11-slim-bookworm

# Не буферизуем вывод Python
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Системные зависимости (для psycopg2 и пр.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY req.txt /app/
RUN pip install --upgrade pip && pip install -r req.txt

# Копируем исходники приложения
COPY . /app/

# Пробрасываем порт
EXPOSE 8000

# Запускаем встроенный Django-сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
