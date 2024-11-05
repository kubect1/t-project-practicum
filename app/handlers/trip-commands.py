from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
import datetime as dt


from app.keyboards.builders import reply_builder
from app.keyboards.reply import rmk, selection_notification_time


from app.curd.trip import create_trip, get_trip_by_id, update_trip_by_id, get_trips_by_chatid
from app.schemas.trip import TransportEnum, TripBase

from app.utils.state import PlanTrip, TripMenu, MainMenu
from app.utils.navigation_states import to_menu_bar, to_modify_trip, to_delete_trip, to_mark_traveled, to_selected_trip_bar
from app.utils.validation import check_validation_string, check_validation_travel_datetime, \
    check_validation_notification_time, check_validation_transport_type, check_validation_trip_exists

router = Router(name="trip_commands_router")

@router.message(MainMenu.planned_trips_bar)
async def command_choose_trip(message: Message, session: AsyncSession, state: FSMContext):
    match message.text:
        case 'Return':
            await to_menu_bar()
    if await check_validation_trip_exists(trips, message.text - 1):
        selected_trip = await get_trip_by_id(trips[message.text - 1])
        await state.update_data(trip=selected_trip)
        await to_selected_trip_bar()
    else:
        await message.answer("Wrong trip id, try again")
        await to_menu_bar()


@router.message(TripMenu.selected_trip_bar)
async def command_choose_action_with_trip(message: Message, session: AsyncSession, state: FSMContext):
    match message.text:
        case 'Change trip':
            await to_modify_trip(message, state)
        case 'Delete trip':
            await to_delete_trip(message, state)
        case 'Mark as travelled':
            await to_mark_traveled(message, state)
        case 'Return':
            await to_menu_bar(message, state)

@router.message(TripMenu.modify_trip)
async def command_modify_trip(message: Message, session: AsyncSession, state: FSMContext):
    pass

@router.message(TripMenu.delete_trip)
async def command_delete_trip(message: Message, session: AsyncSession, state: FSMContext):
    pass

@router.message(TripMenu.mark_traveled)
async def command_mark_travelled(message: Message, session: AsyncSession, state: FSMContext):
    pass