from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.utils.state import MainMenu
from app.keyboards.reply import main_kb
from app.keyboards.builders import default_builder


async def to_menu_bar(message: Message, state: FSMContext):
    await state.set_state(MainMenu.menu_bar)
    await message.answer("Choose an action", reply_markup=main_kb)

async def to_registration(message: Message, state: FSMContext):
    await state.set_state(MainMenu.registration)
    await message.answer(
        "Enter your name",
        reply_markup=default_builder(message.from_user.first_name)
    )

async def to_plan_trip(message: Message, state: FSMContext):
    await state.set_state(MainMenu.plan_trip)
    # add request data about trip

async def to_planned_trip_bar(message: Message, state: FSMContext):
    await state.set_state(MainMenu.planned_trips_bar)
    # add choose trip or return to main menu