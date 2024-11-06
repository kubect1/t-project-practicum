from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.schemas.trip import TripRead
from app.utils.state import MainMenu, PlanTrip, TripMenu, State
from app.keyboards.reply import main_kb, rmk, trip_kb, confirm_kb
from app.keyboards.builders import reply_builder
from sqlalchemy.ext.asyncio import AsyncSession


from app.curd.trip import get_trips_by_chat_id



async def to_menu_bar(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(MainMenu.menu_bar)
    await message.answer("Choose an action", reply_markup=main_kb)

async def to_registration(message: Message, state: FSMContext):
    await state.set_state(MainMenu.registration)
    await message.answer(
        "Enter your name",
        reply_markup=reply_builder(message.from_user.first_name)
    )

async def to_plan_trip(message: Message, state: FSMContext):
    await state.set_state(PlanTrip.from_place_title)
    await message.answer('Enter starting place', reply_markup=rmk)


async def to_planned_trip_bar(message: Message, session: AsyncSession, state: FSMContext):
    trips = await get_trips_by_chat_id(message.from_user.id, session)
    trips = [TripRead.model_validate(trip) for trip in trips]
    await state.update_data(trips=trips)
    if len(trips):
        trips_to_print = str('\n' + 10*'-' + '\n').join([f"{i + 1}: " + str(trips[i]) for i in range(len(trips))])
        await message.answer(trips_to_print)
        await message.answer("Enter number of trip or press button to return", reply_markup=reply_builder('Return'))
        await state.set_state(MainMenu.planned_trips_bar)
    else:
        await message.answer('No trips to print')
        await to_menu_bar(message, state)



async def to_selected_trip_bar(message: Message, state: FSMContext):
    await state.set_state(TripMenu.selected_trip_bar)
    await message.answer("Choose action with a trip", reply_markup=trip_kb)

async def to_modify_trip(message: Message, state: FSMContext):
    await state.set_state(TripMenu.modify_trip)

async def to_delete_trip(message: Message, state: FSMContext):
    await state.set_state(TripMenu.delete_trip)
    await message.answer("Confirm action?", reply_markup=confirm_kb)

async def to_mark_traveled(message: Message, state: FSMContext):
    await state.set_state(TripMenu.mark_traveled)
    await message.answer("Confirm action?", reply_markup=confirm_kb)