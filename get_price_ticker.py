import logging
import requests
import os

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
        return None, err.response.status_code  # Возвращаем код ошибки
    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException: {e}")
        return None, 400  # Общая ошибка

    if "price" in data:
        price = data["price"]
        logger.info(f"Получена цена USDT/RUB: {price}")
        return price, None
    else:
        logger.warning("Ключ 'price' отсутствует в ответе")
        return None, 400  # Ошибка, если цена не найдена

def get_rub_usdt_price():
    params = {
        "symbol": "USDTRUB"  # Торговая пара USDT/RUB
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на HTTP ошибки
        data = response.json()
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTPError: {err}")
        return None, err.response.status_code  # Возвращаем код ошибки
    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException: {e}")
        return None, 400  # Общая ошибка

    if "price" in data:
        try:
            usdt_rub_price = float(data["price"])
            rub_usdt_price = 1 / usdt_rub_price
            logger.info(f"Получена цена RUB/USDT: {rub_usdt_price}")
            return rub_usdt_price, None  # Возвращаем цену и None для ошибок
        except ZeroDivisionError:
            logger.error("Ошибка: деление на ноль")
            return None, 400  # Ошибка деления на ноль
        except ValueError:
            logger.error("Ошибка: некорректное значение для 'price'")
            return None, 400  # Ошибка преобразования значения
    else:
        logger.warning("Ключ 'price' отсутствует в ответе")
        return None, 400  # Ошибка, если цена не найдена
