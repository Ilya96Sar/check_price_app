# Check Price App

**Check Price App** – это Flask-приложение, которое позволяет получать и отображать актуальные курсы конверсии криптовалют USDT/RUB и RUB/USDT с использованием API Binance

## 📋 Описание проекта

Приложение периодически обновляет курсы валют, используя встроенный планировщик задач, и отображает их на веб-странице. Приложение завернуто в Docker-контейнер для удобства развёртывания

## 📂 Структура проекта

/check_price_ticker
    ├── app.py
    ├── get_price_ticker.py
    ├── static
    │   └── styles.css
    └── templates
        └── index.html

### Описание файлов

- **app.py**: Основной файл приложения Flask
- **get_price_ticker.py**: Скрипт для получения курсов валют
- **static/**: Каталог для статических файлов
  - **styles.css**: Файл стилей для приложения
- **templates/**: Каталог для шаблонов HTML
  - **index.html**: Основной HTML-шаблон для отображения информации

## 🚀 Запуск проекта в Docker

### Требования

- Docker
- Git

### Шаги для запуска

1. **Склонируйте репозиторий:**

   ```bash
   git clone https://github.com/Ilya96Sar/check_price_app.git

2. **Перейдите в каталог проекта:**

   ```bash
   cd check_price_app

3. **Постройте Docker образ:**

   ```bash
   docker build -t check_price_app .

4. **Запустите контейнер:**

   ```bash
   docker run -d --env-file .env -p 5000:5000 --name flask_api_appp check_price_app_v2

3. **Перейдите в браузере по адресу:**

   http://localhost:5000/<маршрут из описания>, чтобы увидеть веб-интерфейс приложения.

### Для скачивания Docker-образа и запуска приложения:

Вы можете скачать Docker-образ из Docker Hub. Для этого выполните следующую команду:

    ```bash
    docker pull ilya96sar/check_price_app_v2:latest

Чтобы запустить приложение, выполните следующую команду:

    ```bash
    docker run -d --env-file .env --name flask_api_app -p 5000:5000 ilya96sar/check_price_app_v2:latest

## 📄 Логирование

Приложение сохраняет логи в папке app/logs внутри контейнера. Если вы хотите вывести логи в директорию хоста, используйте флаг -v при запуске контейнера:

    ```bash
    docker run -d -p 5000:5000 --name flask_api_app -v ~/log:/app/logs check_price_app

## 📄 ⚙️ Подключение и конфигурация

Для корректной работы приложения убедитесь, что у вас есть доступ к API Binance.

## 🛠️ Инструменты и технологии

Flask – веб-фреймворк Python.
Docker – контейнеризация для легкого развертывания.
Binance API – получение данных о курсах валют.

## OpenApi Схема

В каталоге находится файл openapi_app.json c API Описанием
