import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from tgbot.config import load_config


config = load_config(".env")

async def auf_status(user_id):
    base = psycopg2.connect(config.db.db_uri, sslmode="require")
    cur = base.cursor() 
    cur.execute("SELECT * FROM users WHERE telegram_id = %s", (str(user_id),))
    user = cur.fetchall()
    answer = False
    if user:
        print('user in system')
        answer = True
    return answer