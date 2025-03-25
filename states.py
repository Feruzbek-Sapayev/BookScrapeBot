from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    main = State()
    send_message = State()