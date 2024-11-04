from flask import Flask, render_template, redirect, jsonify
from get_price_ticker import get_usdt_rub_price, get_rub_usdt_price
import signal
from flask_caching import Cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import sys

load_dotenv()  # Загружаем переменные окружения из .env файла

# Класс конфигурации с Pydantic, без значений по умолчанию
class Config(BaseSettings):
    CACHE_TYPE: str
    CACHE_DEFAULT_TIMEOUT: int

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Создаём экземпляр конфигурации
config = Config()

app = Flask(__name__)

# Загружаем конфигурацию в Flask из Pydantic Config
app.config.from_mapping(config.dict())

# Инициализация кэша
cache = Cache(app)

# Маршрут для курса конверсии USDT/RUB
@app.route('/usdtrub')
def usdt_to_rub():
    price1, error_code = get_usdt_rub_price()
    if error_code is not None:
        return render_template('index.html', error="Не удалось получить цену"), error_code
    return render_template('index.html', price1=price1, page='usdt_to_rub')

# Маршрут для курса конверсии RUB/USDT
@app.route('/rubusdt')
def rub_to_usdt():
    price2, error_code = get_rub_usdt_price()
    if error_code is not None:
        return render_template('index.html', error="Не удалось получить цену"), error_code
    return render_template('index.html', price2=price2, page='rub_to_usdt')

# Маршрут на главную страницу криптобиржи Binance
@app.route('/')
def info_binance():
    return redirect("https://www.binance.com", code=302)



# Обработчик ошибки 400 (Неправильный запрос)
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": "Запрос не может быть разобран или в нем "
                                                       "отсутствуют необходимые параметры"}), 400

# Обработчик ошибки 404 (Страница не найдена)
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": "Запрошенный ресурс не найден"}), 404

# Обработчик ошибки 405 (Метод не разрешён)
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method Not Allowed", "message": "Метод недопустим для запрошенного URL"}), 405

# Обработчик ошибки 429 (Слишком много запросов)
@app.errorhandler(429)
def too_many_requests(error):
    return jsonify({"error": "Too Many Requests", "message": "Вы превысили лимит запросов"}), 429


@app.route('/api/usdttorub', methods=['GET'])
@cache.cached(timeout=config.CACHE_DEFAULT_TIMEOUT)
def func_usdtrub():
    price = get_usdt_rub_price()
    if price is None:
        return jsonify({"Курс": "Цена недоступна"}), 404
    return jsonify({"Курс конверсии USDT/RUB": price})

@app.route('/api/rubtousdt', methods=['GET'])
@cache.cached(timeout=config.CACHE_DEFAULT_TIMEOUT)
def func_rubusdt():
    price = get_rub_usdt_price()
    if price is None:
        return jsonify({"Курс": "Цена недоступна"}), 404
    return jsonify({"Курс конверсии RUB/USDT": price})

def graceful_exit(signum, frame):
    print("Завершение работы приложения...")
    sys.exit(0)

# Обработка сигналов для остановки приложения
signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

# Запуск приложения
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
