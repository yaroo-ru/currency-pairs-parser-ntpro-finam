from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

from datetime import datetime

import pytz  # Для работы с временными зонами

from db import finam


options = Options()
# options.add_argument('--headless')  # Если нужно фоновое выполнение
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

try:
    while True:
        # Получаем текущее московское время
        moscow_tz = pytz.timezone("Europe/Moscow")
        current_time = datetime.now(moscow_tz)

        # Проверяем, находится ли текущее время в диапазоне с 10:00 до 24:00
        if 10 <= current_time.hour < 24:
            # Открываем страницу, если она ещё не открыта
            if driver.current_url != 'https://www.finam.ru/topic/interbank-market/':
                while True:
                    try:
                        driver.get('https://www.finam.ru/topic/interbank-market/')
                        break
                    except:
                        continue

            result = []
            should_continue = False

            # Ищем элементы с курсами валют (класс 'font-2xl')
            prices = driver.find_elements(By.CLASS_NAME, 'font-2xl')[:6]

            # Проверяем, что все значения курса корректные (не равны '--')
            for i in prices:
                if i.text == '--':
                    should_continue = True
                else:
                    print(i.text)

            # Если все значения валидные, сохраняем их в базу
            if not should_continue:
                try:
                    result = [i.text for i in prices][:6]
                    result.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    if len(result) > 2:
                        print(result)
                        finam(result)  # Сохранение данных
                except:
                    print("Ошибка")

                # Ожидание перед следующим запросом
                time.sleep(20)

        else:
            print(f"Парсинг не осуществляется. Текущее московское время: {current_time.strftime('%Y-%m-%d %H:%M:%S')} — вне диапазона с 10:00 до 24:00")

        time.sleep(20)  # Интервал между циклами парсинга
finally:
    # Закрываем веб-драйвер после завершения
    driver.quit()