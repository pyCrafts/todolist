# Используем базовый образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /opt/todolist

# Устанавливаем переменные окружения
ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PYTHONPATH=/opt/todolist

# Создаем систему пользователя и группы
RUN groupadd --system service && useradd --system -g service api

# Копируем файлы конфигурации для pip
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копируем исходный код и скрипт запуска
COPY src/ ./
COPY entrypoint.sh ./entrypoint.sh

# Обновляем права на скрипт запуска и настраиваем пользователя
RUN chmod +x entrypoint.sh
USER api

# Определяем команду запуска
ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Открываем порт для доступа
EXPOSE 8000
