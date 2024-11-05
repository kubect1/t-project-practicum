from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from app.curd.trip import get_trips_by_chatid
from app.utils.state import MainMenu, TripMenu
from app.keyboards.keybords import main_kb


async def to_menu_bar(message: Message, state: FSMContext):
    await state.set_state(MainMenu.menu_bar)
    await message.answer("Choose an action", reply_markup=main_kb)

async def to_planned_trip_bar(message: Message, session: AsyncSession, state: FSMContext):
    trips = await get_trips_by_chatid(message.from_user.id, session)
    if (len(trips) != 0):
        counter = 0
        for trip in trips:
            trip_str = await f"{counter}: " + str(trip)
        trips_to_print = await str('\n' + 10*'-' + '\n').join(trips)
        await message.answer(trips_to_print)
    else:
        await message.answer('No trips to print')
    await state.set_state(MainMenu.planned_trips_bar)
    await message.answer("Choose trip to change")

async def to_selected_trip_bar(message: Message, state: FSMContext):
    await state.set_state(TripMenu.selected_trip_bar)
    await message.answer("Choose action with a trip")

async def to_modify_trip(message: Message, state: FSMContext):
    await state.set_state(TripMenu.modify_trip)

async def to_delete_trip(message: Message, state: FSMContext):
    await state.set_state(TripMenu.delete_trip)

async def to_mark_traveled(message: Message, state: FSMContext):
    await state.set_state(TripMenu.mark_traveled)