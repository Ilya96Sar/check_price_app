import logging
import requests

# Настройка логирования
logging.basicConfig(filename='/app/logs/app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s '
                                                                    '- %('
                                                                'message)s')
logger = logging.getLogger("logger_app")

url = "https://api.binance.com/api/v3/ticker/price"

def get_usdt_rub_price():
    params = {
        "symbol": "USDTRUB"  # Торговая пара USDT/RUB
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на HTTP ошибки
        data = response.json()
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTPError: {err}")
        return None  # Возвращаем только None при ошибке
    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException: {e}")
        return None  # Возвращаем только None при ошибке

    if "price" in data:
        price = float(data["price"])  # Преобразуем цену в float
        logger.info(f"Получена цена USDT/RUB: {price}")
        return price  # Возвращаем только цену
    else:
        logger.warning("Ключ 'price' отсутствует в ответе")
        return None  # Возвращаем None, если цена не найдена

def get_rub_usdt_price():
    usdt_rub_price = get_usdt_rub_price()  # Получаем цену USDT/RUB
    if usdt_rub_price is None:
        return None  # Если цена не получена, возвращаем None

    try:
        rub_usdt_price = 1 / usdt_rub_price
        logger.info(f"Получена цена RUB/USDT: {rub_usdt_price}")
        return rub_usdt_price  # Возвращаем цену RUB/USDT
    except ZeroDivisionError:
        logger.error("Ошибка: Деление на ноль при расчете RUB/USDT")
        return None  # Возвращаем None при делении на ноль
