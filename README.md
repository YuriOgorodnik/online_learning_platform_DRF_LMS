Платформа для онлайн приложения - бэкенд-часть веб-приложения (online_learning_platform)

Описание

    - Настроен CORS.
    - Настроена интеграция с Stripe.
    - Реализована пагинация (с выводом по 1 курсу и уроку на страницу).
    - Реализованы валидаторы:
        Для видео урока можно добавлять ссылку только на контент www.youtube.com
    - Описаны права доступа:
        Каждый пользователь имеет доступ только к своим курсам и урокам по механизму CRUD.
        Пользователь может изменять только свой профиль.
    - Имеется список зависимостей.
    - Документация проекта: http://127.0.0.1:8000/swagger/

Технологии

    - Python
    - Django, DRF
    - JWT, DRF-YASG
    - PostgreSQL
    - Celery, Redis
    - Stripe

Сущности

    - Course (курсы)
    - Lesson (уроки)
    - Users (пользователи)
    - Payment (платежи)
    - Subscription (обновление подписок)

Запуск проекта в Docker:

    Для работы с переменными окружения необходимо создать файл .env и заполнить его согласно файлу .env.example:

        SECRET_KEY=

        POSTGRES_HOST=db
        POSTGRES_DB=
        POSTGRES_USER=
        POSTGRES_PASSWORD=
        POSTGRES_PORT=5432

        STRIPE_API_KEY=

        EMAIL_HOST_USER=
        EMAIL_HOST_PASSWORD=

        CELERY_BROKER_URL=redis://redis:6379
        CELERY_RESULT_BACKEND=redis://redis:6379

    Для создания образа из Dockerfile и запуска контейнера запустить команду:

        docker-compose up --build

        или

        docker-compose up -d --build (для запуска в фоновом режиме)

Запуск приложения в локальной сети:

    Для начала необходимо настроить виртуальное окружение и установить все необходимые зависимости с помощью команд:

        python -m venv venv

        source venv/bin/activate

        pip install -r requirements.txt

    Для работы с переменными окружения необходимо создать файл .env и заполнить его согласно файлу .env.sample:

        SECRET_KEY=

        POSTGRES_HOST=localhost
        POSTGRES_DB=
        POSTGRES_USER=
        POSTGRES_PASSWORD=
        POSTGRES_PORT=5432

        STRIPE_API_KEY=

        EMAIL_HOST_USER=
        EMAIL_HOST_PASSWORD=

        CELERY_BROKER_URL=redis://localhost:6379
        CELERY_RESULT_BACKEND=redis://localhost:6379

Выполнить миграции:

    python3 manage.py migrate

Для заполнения БД запустить команду:

    python manage.py add_data

Для запуска Celery на операционной системе Windows:

    celery -A config beat -l info -S django

    celery -A config worker -l info -P eventlet

Для запуска redis:

    redis-cli

Для запуска приложения:

    python manage.py runserver

Для тестирования проекта запустить команду:

    python manage.py test

Для запуска подсчета покрытия и вывода отчет запустить команды:

    coverage run --source='.' manage.py test 

    coverage report
