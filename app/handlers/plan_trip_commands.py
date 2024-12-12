from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.curd.trip import create_trip
from app.keyboards.builders import reply_builder
from app.keyboards.reply import rmk, selection_notification_time
from app.models.transport_enum import TransportEnum
from app.schemas.trip import TripBase, TripRead
from app.schemas.route import Route
from app.utils.additional_trip_info import get_route_info
from app.utils.get_timezone import get_timezone
from app.utils.navigation_states import to_menu_bar
from app.utils.notifiaction import check_need_to_create_task_immediately
from app.utils.state import PlanTrip
from app.utils.validation import check_validation_string, check_validation_travel_datetime, \
    check_validation_notification_time, check_validation_transport_type, check_validation_location

router = Router(name="plan_trip_commands_router")


@router.message(PlanTrip.from_place_title)
async def command_take_from_place_title(message: Message, state: FSMContext):
    if await check_validation_string(message.text, message):
        await state.update_data(from_place_title=message.text)
        await state.set_state(PlanTrip.from_place)
        await message.answer("Send the location of the place with an attachment", reply_markup=rmk)


@router.message(PlanTrip.from_place)
async def command_take_from_place(message: Message, state: FSMContext):
    location = await check_validation_location(message)
    if location:
        await state.update_data(from_place=location)
        await state.set_state(PlanTrip.to_place_title)
        await message.answer("Enter end of trip place", reply_markup=rmk)




@router.message(PlanTrip.to_place_title)
async def command_take_to_place_title(message: Message, state: FSMContext):
    if await check_validation_string(message.text, message):
        await state.update_data(to_place_title=message.text)
        await state.set_state(PlanTrip.to_place)
        await message.answer("Send the location of the place with an attachment", reply_markup=rmk)


@router.message(PlanTrip.to_place)
async def command_take_to_place(message: Message, state: FSMContext):
    location = await check_validation_location(message)
    if location:
        await state.update_data(to_place=location)
        await state.set_state(PlanTrip.travel_date)
        await message.answer('Enter travel date and time in format: "YYYY-MM-DD HH:MM:SS", without quotation marks', reply_markup=rmk)


@router.message(PlanTrip.travel_date)
async def command_take_travel_date(message: Message, state: FSMContext):
    trip_data = await state.get_data()
    tz = get_timezone(trip_data['from_place'])
    datetime = await check_validation_travel_datetime(message.text, tz, message)
    if datetime:
        await state.update_data(travel_date=datetime)
        await state.set_state(PlanTrip.notification_before_travel)
        await message.answer('Enter the time for notification before travel if format: "days hours minutes seconds", '
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
        route = await get_route_info(trip_data['from_place'], trip_data['to_place'], trip_data['transport_type'])
        if route is None:
            route = await get_route_info(trip_data['from_place'], trip_data['to_place'], trip_data['transport_type'])
        if route is None:
            await message.answer("It is impossible to get route")
            await message.answer("Try changing location later")
            route = Route(distance=0, duration=0)
        created_trip = await create_trip(
            new_trip=TripBase(
                chat_id =message.from_user.id,
                create_date=message.date.replace(tzinfo=None),
                isEnded=False,
                route=route,
                **trip_data
            ),
            session=session
        )
        if created_trip is None:
            await message.answer("It is impossible to create trip")
        else:
            created_trip = TripRead.model_validate(created_trip)
            await check_need_to_create_task_immediately(created_trip)
            await message.answer(created_trip.get_info())
            await message.answer("The trip was saved")
        await to_menu_bar(message, state)
