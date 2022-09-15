import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import load_config

config = load_config(".env")

async def postgre_start():
    base = psycopg2.connect(config.db.db_uri, sslmode="require")
    cur = base.cursor()
    if base:
        print('data base connect Ok!')
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        id                      serial
            constraint users_pk
                primary key,
        telegram_id             text not null,
        user_name               varchar(45),
        trial_version_activated boolean default false,
        spreads_on               boolean default false,
        balance_usdt            numeric default 0
    );
    
    DO $$ BEGIN
        IF to_regtype('order_status') IS NULL THEN
            CREATE TYPE order_status AS ENUM ('pending', 'success');
        END IF;
    END $$;
    --DROP TYPE IF EXISTS order_status;
    --CREATE TYPE order_status AS ENUM ('pending', 'success');

    
    create unique index if not exists users_telegram_id_uindex
        on users (telegram_id);
        
        
    create table if not exists user_orders(
        id             serial
            constraint user_orders_pk
                primary key,
        user_id        integer
            constraint user_orders_users_telegram_id_fk
                references users (id),
        order_created  timestamp,
        order_sum_usdt numeric,
        status         order_status
    );  
    
    
    create table if not exists user_subscriptions(
        id       serial
            constraint user_subscriptions_pk
                primary key,
        user_id  integer
            constraint user_subscriptions_users_id_fk
                references users (id),
        valid_to timestamp
    );   
    
    
    create table if not exists promocodes(
        id       serial
            constraint promocodes_pk
                primary key,
        code     varchar(45),
        discount int
    );   
    
    
    create table if not exists spread_directions(
        id   serial
            constraint spread_directions_pk
                primary key,
        name varchar(60)
    );
    
    
    create table if not exists exchanges(
        id   serial
            constraint exchanges_pk
                primary key,
        name varchar(60)
    );
    
    
    create table if not exists banks(
        id   serial
            constraint banks_pk
                primary key,
        name varchar(60)
    );
    
    
    create table if not exists cryptocurrencies(
        id   serial
            constraint cryptocurrencies_pk
                primary key,
        name varchar(60)
    );


    create table if not exists fiat_currencies(
        id   serial
            constraint fiat_currencies_pk
                primary key,
        name varchar(60)
    );


    create table if not exists operation_options(
        id   serial
            constraint operation_options_pk
                primary key,
        name text
    );
    
    
    create table if not exists minimal_spread(
        id               serial
            constraint minimal_spread_pk
                primary key,
        user_id          int
            constraint minimal_spread_users_id_fk
                references users,
        spread_direction int
            constraint minimal_spread_spread_directions_id_fk
                references spread_directions,
        spread_value     int
    );


    create table if not exists is_direction_on_for_user(
        id               serial
            constraint is_direction_on_for_user_pk
                primary key,
        user_id          int
            constraint is_direction_on_for_user_users_id_fk
                references users,
        spread_direction int
            constraint is_direction_on_for_user_spread_directions_id_fk
                references spread_directions,
        is_on            boolean default false
    );
                ''')
    

    base.commit()
    cur.close()
    base.close()


async def postgre_insert_table():
    base = psycopg2.connect(config.db.db_uri, sslmode="require")
    cur = base.cursor()
    if base:
        print('start insert base row')
    # заполнение таблицы spread_directions, базовыми значениями
    cur.execute('''INSERT INTO spread_directions (id, name)
        SELECT 1, 'Найпростіші (Найліквідніші) зв’язки'
        WHERE
            NOT EXISTS (
                SELECT id FROM spread_directions WHERE id = 1
            );
            
        INSERT INTO spread_directions (id, name)
        SELECT 2, 'Міжбіржові'
        WHERE
            NOT EXISTS (
                SELECT id FROM spread_directions WHERE id = 2
            );
            
        INSERT INTO spread_directions (id, name)
        SELECT 3, 'Готівка'
        WHERE
            NOT EXISTS (
                SELECT id FROM spread_directions WHERE id = 3
            );
            
        INSERT INTO spread_directions (id, name)
        SELECT 4, 'Binance'
        WHERE
            NOT EXISTS (
                SELECT id FROM spread_directions WHERE id = 4
            );
            
        INSERT INTO spread_directions (id, name)
        SELECT 5, 'OKX'
        WHERE
            NOT EXISTS (
                SELECT id FROM spread_directions WHERE id = 5
            );
            
        INSERT INTO spread_directions (id, name)
        SELECT 6, 'ByBit'
        WHERE
            NOT EXISTS (
                SELECT id FROM spread_directions WHERE id = 6
            );
            
        INSERT INTO spread_directions (id, name)
        SELECT 7, 'Wise'
        WHERE
            NOT EXISTS (
                SELECT id FROM spread_directions WHERE id = 7
            );
            
        INSERT INTO spread_directions (id, name)
        SELECT 8, 'LocalBitcoins'
        WHERE
            NOT EXISTS (
                SELECT id FROM spread_directions WHERE id = 8
            );
                
                ''')
    
    # заполнение таблицы exchanges, базовыми значениями
    cur.execute('''INSERT INTO exchanges (id, name)
        SELECT 1, 'Binance'
        WHERE
            NOT EXISTS (
                SELECT id FROM exchanges WHERE id = 1
            );
        INSERT INTO exchanges (id, name)
        SELECT 2, 'ByBit'
        WHERE
            NOT EXISTS (
                SELECT id FROM exchanges WHERE id = 2
            );
        INSERT INTO exchanges (id, name)
        SELECT 3, 'OKX'
        WHERE
            NOT EXISTS (
                SELECT id FROM exchanges WHERE id = 3
            );
        INSERT INTO exchanges (id, name)
        SELECT 4, 'WhiteBit'
        WHERE
            NOT EXISTS (
                SELECT id FROM exchanges WHERE id = 4
            );
            ''')
    
    # заполнение таблицы banks, базовыми значениями
    cur.execute('''INSERT INTO banks (id, name)
        SELECT 1, 'ПриватБанк'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 1
            );
        INSERT INTO banks (id, name)
        SELECT 2, 'МоноБанк'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 2
            );
        INSERT INTO banks (id, name)
        SELECT 3, 'СпортБанк'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 3
            );
        INSERT INTO banks (id, name)
        SELECT 4, 'Райфайзен'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 4
            );
        INSERT INTO banks (id, name)
        SELECT 5, 'Пумб'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 5
            );
        INSERT INTO banks (id, name)
        SELECT 6, 'iziБанк'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 6
            );
        INSERT INTO banks (id, name)
        SELECT 7, 'Абанк'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 7
            );
        INSERT INTO banks (id, name)
        SELECT 8, 'Accord'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 8
            );
        INSERT INTO banks (id, name)
        SELECT 9, 'Ощадбанк'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 9
            );
        INSERT INTO banks (id, name)
        SELECT 10, 'OTPБанк'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 10
            );
        INSERT INTO banks (id, name)
        SELECT 11, 'NEO'
        WHERE
            NOT EXISTS (
                SELECT id FROM banks WHERE id = 11
            );
            ''')
    
    # заполнение таблицы cryptocurrencies, базовыми значениями
    cur.execute('''INSERT INTO cryptocurrencies (id, name)
        SELECT 1, 'USDT'
        WHERE
            NOT EXISTS (
                SELECT id FROM cryptocurrencies WHERE id = 1
            );
        INSERT INTO cryptocurrencies (id, name)
        SELECT 2, 'BUSD'
        WHERE
            NOT EXISTS (
                SELECT id FROM cryptocurrencies WHERE id = 2
            );
        INSERT INTO cryptocurrencies (id, name)
        SELECT 3, 'BTC'
        WHERE
            NOT EXISTS (
                SELECT id FROM cryptocurrencies WHERE id = 3
            );
        INSERT INTO cryptocurrencies (id, name)
        SELECT 4, 'BNB'
        WHERE
            NOT EXISTS (
                SELECT id FROM cryptocurrencies WHERE id = 4
            );
        INSERT INTO cryptocurrencies (id, name)
        SELECT 5, 'ETH'
        WHERE
            NOT EXISTS (
                SELECT id FROM cryptocurrencies WHERE id = 5
            );
        INSERT INTO cryptocurrencies (id, name)
        SELECT 6, 'UAH'
        WHERE
            NOT EXISTS (
                SELECT id FROM cryptocurrencies WHERE id = 6
            );
        INSERT INTO cryptocurrencies (id, name)
        SELECT 7, 'SHIB'
        WHERE
            NOT EXISTS (
                SELECT id FROM cryptocurrencies WHERE id = 7
            );
            ''')
    
    # заполнение таблицы fiat_currencies, базовыми значениями
    cur.execute('''INSERT INTO fiat_currencies (id, name)
        SELECT 1, 'EUR'
        WHERE
            NOT EXISTS (
                SELECT id FROM fiat_currencies WHERE id = 1
            );
        INSERT INTO fiat_currencies (id, name)
        SELECT 2, 'GBP'
        WHERE
            NOT EXISTS (
                SELECT id FROM fiat_currencies WHERE id = 2
            );
        INSERT INTO fiat_currencies (id, name)
        SELECT 3, 'PLN'
        WHERE
            NOT EXISTS (
                SELECT id FROM fiat_currencies WHERE id = 3
            );
        INSERT INTO fiat_currencies (id, name)
        SELECT 4, 'USD'
        WHERE
            NOT EXISTS (
                SELECT id FROM fiat_currencies WHERE id = 4
            );
        INSERT INTO fiat_currencies (id, name)
        SELECT 5, 'UAH'
        WHERE
            NOT EXISTS (
                SELECT id FROM fiat_currencies WHERE id = 5
            );
            ''')
    # заполнение таблицы operation_options, базовыми значениями
    cur.execute('''INSERT INTO operation_options (id, name)
        SELECT 1, 'Купуємо крипту, продаємо її'
        WHERE
            NOT EXISTS (
                SELECT id FROM operation_options WHERE id = 1
            );
        INSERT INTO operation_options (id, name)
        SELECT 2, 'Купуємо крипту, міняємо на іншу, продаємо як мейкер'
        WHERE
            NOT EXISTS (
                SELECT id FROM operation_options WHERE id = 2
            );
        INSERT INTO operation_options (id, name)
        SELECT 3, 'Купуємо крипту та продаємо (одна платіжна система)'
        WHERE
            NOT EXISTS (
                SELECT id FROM operation_options WHERE id = 3
            );
        INSERT INTO operation_options (id, name)
        SELECT 4, 'Переводимо на BINANCE та продаємо на P2Р'
        WHERE
            NOT EXISTS (
                SELECT id FROM operation_options WHERE id = 4
            );
        INSERT INTO operation_options (id, name)
        SELECT 5, 'Переводимо на Bybit и продаємо на P2P'
        WHERE
            NOT EXISTS (
                SELECT id FROM operation_options WHERE id = 5
            );
            ''')
    
    
    base.commit()
    cur.close()
    base.close()