from flask import Flask, render_template, redirect
from get_price_ticker import get_usdt_rub_price, get_rub_usdt_price
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import signal
import sys

app = Flask(__name__)

# Глобальные переменные для хранения курса валют
latest_usdt_to_rub = None
latest_rub_to_usdt = None
scheduler_started = False
last_update_usdt_rub = None
last_update_rub_usdt = None

# Функция для обновления курса USDT/RUB
def update_usdt_rub():
    global last_update_usdt_rub
    price, error_code = get_usdt_rub_price()
    if error_code is None:
        last_update_usdt_rub = datetime.utcnow()
        app.logger.info(f"Курс обновлен: {price}, последнее обновление: {last_update_usdt_rub}")
    else:
        app.logger.error(f"Ошибка при обновлении курса: {error_code}")

# Функция для обновления курса RUB/USDT
def update_rub_usdt():
    global latest_rub_to_usdt
    price, error_code = get_rub_usdt_price()
    if error_code is None:
        last_update_rub_usdt = datetime.utcnow()
        app.logger.info(f"Курс обновлен: {price}, последнее обновление: {last_update_rub_usdt}")
    else:
        app.logger.error(f"Ошибка при обновлении курса: {error_code}")

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="Страница не найдена"), 404

# Инициализация и настройка BackgroundScheduler для запуска обновлений
scheduler = BackgroundScheduler()
scheduler.add_job(update_usdt_rub, 'interval', minutes=1)  # Запуск обновления USDT/RUB каждую минуту
scheduler.add_job(update_rub_usdt, 'interval', minutes=1)  # Запуск обновления RUB/USDT каждую минуту
scheduler.start()

# Инициализация BackgroundScheduler при первом запросе
@app.before_request
def setup_scheduler():
    global scheduler_started
    if not scheduler_started:
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_usdt_rub, 'interval', minutes=1)
        scheduler.add_job(update_rub_usdt, 'interval', minutes=1)
        scheduler.start()
        scheduler_started = True
        app.logger.info("Запуск фонового обновления курса валют")

def shutdown_scheduler():
    global scheduler
    if scheduler_started:
        scheduler.shutdown()
        app.logger.info("Шедулер остановлен")

# Обработка сигналов для остановки приложения
signal.signal(signal.SIGINT, lambda s, f: shutdown_scheduler())
signal.signal(signal.SIGTERM, lambda s, f: shutdown_scheduler())

# Запуск приложения
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
