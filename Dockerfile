# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY . /app

# Создаём директорию для логов
RUN mkdir -p /app/logs

# Устанавливаем зависимости
RUN pip install --no-cache-dir Flask requests APScheduler

# Указываем команду для запуска приложения
CMD ["python3", "app.py"]

# Пробрасываем порт
EXPOSE 5000
