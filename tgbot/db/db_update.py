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
    cur.execute("INSERT INTO user_directions_exchanges (user_id) VALUES (%s)",(user[0],))
    
    
    base.commit()
    cur.close()
    base.close()