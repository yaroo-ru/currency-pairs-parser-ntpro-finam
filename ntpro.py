from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from db import ntpro

import time
from datetime import datetime
import pytz
from selenium.common.exceptions import WebDriverException, NoSuchElementException

# Настройки для веб-драйвера (Chrome)
options = Options()
# options.add_argument('--headless')  # Если нужен фоновый режим
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Пытаемся открыть сайт ntprogress.ru
while True:
    try:
        driver.get('https://ntprogress.ru/ru/')
        break
    except:
        continue

time.sleep(3)

# Основной цикл парсинга
while True:
    moscow_tz = pytz.timezone("Europe/Moscow")
    current_time = datetime.now(moscow_tz)

    # Парсинг работает только в интервале с 10:00 до 19:00
    if 10 <= current_time.hour < 19:
        try:
            divs = driver.find_elements(By.CLASS_NAME, 'quoteContainer-0-1-246')
            USDRUB_TOM_bid = divs[0].find_elements(By.TAG_NAME, 'p')[1].text
            USDRUB_TOM_offer = divs[1].find_elements(By.TAG_NAME, 'p')[1].text
            CHNRUB_TOM_bid = divs[2].find_elements(By.TAG_NAME, 'p')[1].text
            CHNRUB_TOM_offer = divs[3].find_elements(By.TAG_NAME, 'p')[1].text
            EURRUB_TOM_bid = divs[4].find_elements(By.TAG_NAME, 'p')[1].text
            EURRUB_TOM_offer = divs[5].find_elements(By.TAG_NAME, 'p')[1].text

            # Сохраняем данные в базу
            try:
                ntpro(USDRUB_TOM_bid, USDRUB_TOM_offer, EURRUB_TOM_bid, EURRUB_TOM_offer, CHNRUB_TOM_bid, CHNRUB_TOM_offer, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            except:
                print('Ошибка при записи в базу, новая попытка через минуту.')
                
        except:
            print(f"Ошибка при получении данных.")
    else:
        print(f"Парсинг не работает. Текущее московское время: {current_time.strftime('%Y-%m-%d %H:%M:%S')} — вне рабочего интервала.")

    time.sleep(60)