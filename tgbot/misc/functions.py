import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from tgbot.config import load_config


config = load_config(".env")

async def auf_status(user_id):
    base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
    cur = base.cursor() 
    cur.execute("SELECT * FROM users WHERE telegram_id = %s", (str(user_id),))
    user = cur.fetchall()
    answer = False
    if user:
        answer = True
    return answer

def get_settings_directions(user_id,spread_direction):
    base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
    cur = base.cursor() 
    cur.execute('''SELECT user_directions_exchanges.exchange_chosen, ub.bank_chosen, us.cryptocurrency_chosen, uo.operation_options_chosen, uf.fiat_currency_chosen
                            FROM user_directions_exchanges
                                LEFT JOIN user_directions_banks ub ON ub.user_id  = user_directions_exchanges.user_id and ub.spread_direction = user_directions_exchanges.spread_direction
                                LEFT JOIN user_directions_cryptocurrency us on us.user_id = user_directions_exchanges.user_id and us.spread_direction = user_directions_exchanges.spread_direction
                                LEFT JOIN user_directions_fiat_currency uf on uf.user_id = user_directions_exchanges.user_id and uf.spread_direction = user_directions_exchanges.spread_direction
                                LEFT JOIN user_directions_operation_options uo on uo.user_id = user_directions_exchanges.user_id and uo.spread_direction = user_directions_exchanges.spread_direction
                                LEFT JOIN users ON users.id = user_directions_exchanges.user_id
                                LEFT JOIN spread_directions ON spread_directions.id = user_directions_exchanges.spread_direction
                        WHERE users.telegram_id = %s and spread_directions.name = %s''', (str(user_id), spread_direction))
    directions = cur.fetchone()
    return directions