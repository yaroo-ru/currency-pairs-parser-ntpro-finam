import psycopg2

# Настройки подключения к базе данных
host = 'localhost'     
port = '5432'          
db_name = 'postgres_db'  
user = 'postgres'     
password = 'root'  

try:
    # Подключение к базе данных
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=db_name,
        user=user,
        password=password
    )
    cursor = connection.cursor()

    # Создание таблицы finam
    create_finam_table = '''
    CREATE TABLE IF NOT EXISTS finam (
        id SERIAL PRIMARY KEY,
        bid_usd_rub VARCHAR(10),
        ask_usd_rub VARCHAR(10),
        bid_eur_rub VARCHAR(10),
        ask_eur_rub VARCHAR(10),
        bid_cny_rub VARCHAR(10),
        ask_cny_rub VARCHAR(10),
        date_time VARCHAR(100)
    )
    '''

    # Создание таблицы ntpro
    create_ntpro_table = '''
    CREATE TABLE IF NOT EXISTS ntpro (
        id SERIAL PRIMARY KEY,
        bid_usd_rub VARCHAR(10),
        offer_usd_rub VARCHAR(10),
        bid_eur_rub VARCHAR(10),
        offer_eur_rub VARCHAR(10),
        bid_chn_rub VARCHAR(10),
        offer_chn_rub VARCHAR(10),
        date_time VARCHAR(100)
    )
    '''

    # Выполнение запросов создания таблиц
    cursor.execute(create_finam_table)
    cursor.execute(create_ntpro_table)
    connection.commit()

    print("Таблицы успешно созданы!")
    
except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()

# Функция для записи данных в таблицу finam
def finam(*args):
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=db_name,
        user=user,
        password=password
    )
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO finam (bid_usd_rub, ask_usd_rub, bid_eur_rub, ask_eur_rub, bid_cny_rub, ask_cny_rub, date_time) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.executemany(insert_query, args)
    connection.commit()

    cursor.close()
    connection.close()

# Функция для записи данных в таблицу ntpro
def ntpro(*args):
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=db_name,
        user=user,
        password=password
    )
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO ntpro (bid_usd_rub, offer_usd_rub, bid_eur_rub, offer_eur_rub, bid_chn_rub, offer_chn_rub, date_time) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, args)
    connection.commit()

    cursor.close()
    connection.close()