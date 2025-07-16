# **Todolist**

Простой To-Do List приложение, разработанное с использованием Django и Django REST Framework. Позволяет создавать, просматривать, обновлять и удалять задачи, категории, комментарии и доски через REST API. Проект упакован в Docker-контейнеры для удобного развёртывания.

## Содержание

- [Особенности](#особенности)
- [Технологии](#технологии)
- [Установка и запуск](#установка-и-запуск)
- [Конфигурация](#конфигурация)
- [API](#api)

## Особенности

- CRUD операции для задач, категорий, комментариев и досок
- Фильтрация и пагинация списков
- Авторизация и управление пользователями (регистрация, вход, профиль, смена пароля)
- Интеграция с PostgreSQL
- Развёртывание через Docker Compose

## Технологии

- Python 3.11
- Django 5.0
- Django REST Framework
- PostgreSQL
- Docker, Docker Compose

## Установка и запуск

### С помощью Docker

1. Клонируйте репозиторий и перейдите в каталог проекта:
   ```bash
   git clone https://github.com/pyCrafts/todolist.git
   cd todolist
   ```
2. В корне проекта создайте файл `.env` (см. раздел [Конфигурация](#конфигурация)).
3. Запустите контейнеры:
   ```bash
   docker-compose up --build
   ```
4. Откройте в браузере:
   - API: [http://localhost:8000/](http://localhost:8000/)

### Локальная установка

1. Клонируйте репозиторий и перейдите в каталог проекта.
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Настройте PostgreSQL и создайте базу данных.
5. В корне проекта создайте файл `.env` (см. раздел [Конфигурация](#конфигурация)).
6. Выполните миграции и запустите сервер:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
7. Перейдите в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Конфигурация

Создайте в корне проекта файл `.env` со следующими переменными:

```ini
PYTHONPATH=src
SECRET_KEY='<ваш_секретный_ключ>'
DEBUG=True
URL_WEBSITE='http://localhost:8000'
DATABASE_USER='<имя_пользователя>'
POSTGRES_PASSWORD='<пароль>'
DATABASE_DB='<имя_базы_данных>'
```

Убедитесь, что переменные соответствуют настройкам в `docker-compose.yml` или локальному окружению.

## API

### Пользователи (core)

- `POST /core/signup/` — регистрация пользователя `[name='signup']`
- `POST /core/login/` — вход пользователя `[name='login']`
- `GET, PUT, PATCH, DELETE /core/profile/` — получить, обновить или удалить профиль пользователя `[name='update-retrieve-destroy-user']`
- `POST /core/update_password/` — смена пароля пользователя `[name='update-password']`

### Категории (goals/goal_category)

- `POST /goals/goal_category/create/` — создать категорию `[name='create-category']`
- `GET /goals/goal_category/list/` — список категорий `[name='cat-list']`
- `GET, PUT, PATCH, DELETE /goals/goal_category/<pk>/` — детали категории `[name='cat_detail']`

### Цели (goals/goal)

- `POST /goals/goal/create/` — создать цель `[name='goal-create']`
- `GET /goals/goal/list/` — список целей `[name='goal-list']`
- `GET, PUT, PATCH, DELETE /goals/goal/<pk>/` — детали цели `[name='goal-detail']`

### Комментарии к целям (goals/goal_comment)

- `POST /goals/goal_comment/create/` — добавить комментарий `[name='create-comment']`
- `GET /goals/goal_comment/list/` — список комментариев `[name='comment-list']`
- `GET, PUT, PATCH, DELETE /goals/goal_comment/<pk>/` — детали комментария `[name='comment-detail']`

### Доски (goals/board)

- `POST /goals/board/create/` — создать доску `[name='board-create']`
- `GET /goals/board/list/` — список досок `[name='board-list']`
- `GET, PUT, PATCH, DELETE /goals/board/<pk>/` — детали доски `[name='board-detail']`
