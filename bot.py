import asyncio
import logging
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from tgbot.config import load_config
from tgbot.handlers.admin import admin_router
from tgbot.handlers.user import user_router
from tgbot.handlers.system_callback import system_callback_router
from tgbot.handlers.user_settings import user_settings_router
from tgbot.handlers.choose_directions import choose_directions_router
from tgbot.handlers.settings_directions import settings_directions_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.db import start_db
from tgbot.services import broadcaster
from tgbot.misc.functions import mailing,check_sub

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))


async def main():
    await start_db.postgre_start()
    await start_db.postgre_insert_table()
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    for router in [
        admin_router,
        user_router,
        user_settings_router,
        system_callback_router,
        choose_directions_router,
        settings_directions_router,
    ]:
        dp.include_router(router)

    register_global_middlewares(dp, config)

    await on_startup(bot, config.tg_bot.admin_ids)
    await asyncio.gather(check_sub(),dp.start_polling(bot), mailing())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")
