import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import load_config

config = load_config(".env")

async def register_user(user_id,user_name):
    base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
    cur = base.cursor()
    
    cur.execute("INSERT INTO users (telegram_id, user_name) VALUES (%s, %s)",(user_id,user_name))
    base.commit()
    
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    i = 1
    while i < 9:
        cur.execute("INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen) VALUES (%s,%s,%s)",(user[0],i,[]))
        i += 1
    i = 1
    while i < 9:
        cur.execute("INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen) VALUES (%s,%s,%s)",(user[0],i,[]))
        i += 1
    i = 1
    while i < 9:
        cur.execute("INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen) VALUES (%s,%s,%s)",(user[0],i,[]))
        i += 1
    i = 1
    while i < 9:
        cur.execute("INSERT INTO user_directions_fiat_currency (user_id,spread_direction,fiat_currency_chosen) VALUES (%s,%s,%s)",(user[0],i,[]))
        i += 1
    i = 1
    while i < 9:
        cur.execute("INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen) VALUES (%s,%s,%s)",(user[0],i,[]))
        i += 1

    i = 1
    while i < 9:
        cur.execute("INSERT INTO minimal_spread (user_id,spread_direction) VALUES (%s,%s)",(user[0],i))
        i += 1
    i = 1
    while i < 9:
        cur.execute("INSERT INTO is_direction_on_for_user (user_id,spread_direction) VALUES (%s,%s)",(user[0],i))
        i += 1
    
    
    
    base.commit()
    cur.close()
    base.close()