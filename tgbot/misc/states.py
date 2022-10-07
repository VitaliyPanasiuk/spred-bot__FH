from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup


class exmple_state(StatesGroup):
    name = State()
    age = State()
    
class min_spread_state(StatesGroup):
    num = State()
    direction = State()
    id = State()
    
class promo_state(StatesGroup):
    name = State()
    id = State()
