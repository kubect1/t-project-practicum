from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.utils.state import MainMenu
from app.keyboards.keybords import main_kb


async def to_menu_bar(message: Message, state: FSMContext):
    await state.set_state(MainMenu.menu_bar)
    await message.answer("Choose an action", reply_markup=main_kb)