# Тестовое задание: Веб-сервер для обработки платёжных транзакций

## Описание
Проект представляет собой Django-приложение с двумя административными панелями:

- **Wagtail**
- **Django Unfold Admin**

Всё взаимодействие осуществляется исключительно через эти панели.

## Необходимые инструменты

- Docker и Docker Compose (версия 3.8+)

---

## Шаг 1. Создание файла `.env` по подобию .env_example

> При необходимости скорректируйте переменные под ваши настройки.

---

## Шаг 2. Конфигурация `docker-compose.yml`

Используется версия `3.8`. Сервисы:

- **postgresql-service** — PostgreSQL 17 с tmpfs-хранилищем данных (каждая перезагрузка — чистая БД).
- **redis-stack-server** — Redis Stack в качестве брокера задач.
- **minio-s3-srv** — MinIO для S3-совместимого хранения статики.
- **backend-django-main-app-service** — Django-приложение: миграции + `runserver`.
- **celery-worker** — Celery Worker для выполнения задач.
- **celery-beat** — Celery Beat для планировщика задач.
- **flower** — Веб-интерфейс для мониторинга Celery.

---

## Шаг 3. Запуск проекта

В корне репозитория выполните:

```bash
docker-compose up -d --build
```

Это создаст и запустит контейнеры для всех сервисов.

```bash
docker-compose ps
```

---

## Шаг 4. Настройка MinIO

1. Откройте консоль MinIO по адресу: http://localhost:9001
2. Введите credentials из `.env`.
3. Создайте бакет с именем `s3bucket` и сделайте его публичным.

---

## Шаг 5. Первичная настройка Django

1. Соберите статические файлы:

    ```bash
    docker-compose exec backend-django-main-app-service python manage.py collectstatic
    ```

2. Создайте суперпользователя:

    ```bash
    docker-compose exec backend-django-main-app-service python manage.py createsuperuser
    ```

---

## Шаг 6. Доступ к административным панелям

- **Django Admin**: http://localhost:8000/cms/
- **Unfold Admin**: http://localhost:8000/admin/

Используйте учётные данные суперпользователя.

---

## Дополнительные возможности

- Автоматическая смена статуса счёта на “просрочен” через Celery Beat.
- Цветовая маркировка и фильтрация статусов в обеих админках.
- Ограничение выбора счетов при создании Попытки оплаты.
- Dashboard в Unfold Admin с отображением количества записей по статусам.

---

**Успешной работы с проектом!**

