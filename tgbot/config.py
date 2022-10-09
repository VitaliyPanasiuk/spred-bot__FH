from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    db_uri: str


@dataclass
class TgBot:
    token: str
    token2: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token='5632625717:AAG9K-ODI4emMk5JslSzGuQFr8pEjHlYeYc',
            token2='5663714794:AAEDjs21ftXsJh_1wMIWfT83x_7N1rSKPr0',
            admin_ids=(),
            use_redis=False,
        ),
        db=DbConfig(
            host='localhost',
            password='27052004',
            user='postgres',
            database='postgres',
            db_uri = ''
        ),
        misc=Miscellaneous()
    )
