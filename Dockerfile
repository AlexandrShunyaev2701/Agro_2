FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/opt/venv
RUN pip install --upgrade pip virtualenv \
    && virtualenv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY req.txt /app/
RUN pip install --no-cache-dir -r req.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
