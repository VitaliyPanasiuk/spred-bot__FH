import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import load_config

config = load_config(".env")

async def register_user(user_id,user_name):
    base = psycopg2.connect(config.db.db_uri, sslmode="require")
    cur = base.cursor()
    
    cur.execute("INSERT INTO users (telegram_id, user_name) VALUES (%s, %s)",(user_id,user_name))
    # cur.execute("INSERT INTO user_subscriptions (user_id, valid_to) VALUES (%s, %s)",(user_id,'0000-00-00 00:00:00'))
    # cur.execute("INSERT INTO minimal_spread (user_id,spread_value) VALUES (%s, %s)",(user_id,0))
    # cur.execute("INSERT INTO is_direction_on_for_user (user_id, spread_direction,is_on) VALUES (%s, %s, %s)",(user_id,'false',False))
    
    base.commit()
    cur.close()
    base.close()