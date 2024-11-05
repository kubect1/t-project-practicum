from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
import datetime as dt


from app.keyboards.builders import reply_builder
from app.keyboards.reply import rmk, selection_notification_time


from app.curd.trip import create_trip, get_trip_by_id, update_trip_by_id
from app.schemas.trip import TransportEnum, TripBase

from app.utils.state import PlanTrip
from app.utils.navigation_states import to_menu_bar
from app.utils.validation import check_validation_string, check_validation_travel_datetime, \
    check_validation_notification_time, check_validation_transport_type

router = Router(name="trip_commands_router")


@router.message(PlanTrip.from_place_title)
async def command_take_from_place_title(message: Message, state: FSMContext):
    if await check_validation_string(message.text, message):
        await state.update_data(from_place_title=message.text)
        await state.set_state(PlanTrip.to_place_title)
        await message.answer("Enter end of trip place", reply_markup=rmk)


@router.message(PlanTrip.to_place_title)
async def command_take_to_place_title(message: Message, state: FSMContext):
    if await check_validation_string(message.text, message):
        await state.update_data(to_place_title=message.text)
        await state.set_state(PlanTrip.travel_date)
        await message.answer('Enter travel date and time in format: "YYYY-MM-DD HH:MM:SS", without quotation marks', reply_markup=rmk)


@router.message(PlanTrip.travel_date)
async def command_take_travel_date(message: Message, state: FSMContext):
    datetime = await check_validation_travel_datetime(message.text, message)
    if datetime:
        await state.update_data(travel_date=datetime)
        await state.set_state(PlanTrip.notification_before_travel)
        await message.answer('Enter the time for notification if format: "days hours minutes seconds", '
                             'without quotation marks where you write numbers instead of words', reply_markup=selection_notification_time)


@router.message(PlanTrip.notification_before_travel)
async def command_take_notification_before_travel(message: Message, state: FSMContext):
    datetime = await check_validation_notification_time(message.text, message)
    if datetime:
        await state.update_data(notification_before_travel=datetime)
        await state.set_state(PlanTrip.transport_type)
        await message.answer(
            "Choose type of transport",
                 reply_markup=reply_builder([TransportEnum(transport_type).name for transport_type in list(TransportEnum)])
                )


@router.message(PlanTrip.transport_type)
async def command_take_transport_type(message: Message, session: AsyncSession, state: FSMContext):
    if await check_validation_transport_type(message.text, message):
        await state.update_data(transport_type=TransportEnum(getattr(TransportEnum, message.text)))
        trip_data = await state.get_data()
        await state.clear()
        created_trip = await create_trip(
            new_trip=TripBase(
                chat_id =message.from_user.id,
                to_place={},
                from_place={},
                create_date=message.date.replace(tzinfo=None),
                isEnded=False,
                **trip_data
            ),
            session=session
        )
        if created_trip is None:
            await message.answer("It is impossible to create trip")
        else:
            # change data for to show the user
            trip_data['transport_type'] = trip_data['transport_type'].name
            trip_data['notification_before_travel'] = trip_data['notification_before_travel'] - dt.datetime.fromisoformat('1970-01-01')
            text = '\n'.join([f'{key}: {value}' for key, value in trip_data.items()])
            await message.answer(text)
            await message.answer("The trip was saved")
        await to_menu_bar(message, state)




