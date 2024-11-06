from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
import datetime as dt

from app.keyboards.builders import reply_builder
from app.keyboards.reply import rmk, selection_notification_time

from app.curd.trip import create_trip, update_trip_by_id, delete_trip_by_id
from app.schemas.trip import TransportEnum, TripBase, TripRead

from app.utils.state import PlanTrip, TripMenu, MainMenu
from app.utils.navigation_states import to_menu_bar, to_modify_trip, to_delete_trip, to_mark_traveled, to_selected_trip_bar, \
    to_planned_trip_bar
from app.utils.validation import check_validation_string, check_validation_travel_datetime, \
    check_validation_notification_time, check_validation_transport_type, check_validation_number_of_trip


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



@router.message(MainMenu.planned_trips_bar)
async def command_choose_trip(message: Message, session: AsyncSession, state: FSMContext):
    state_data = await state.get_data()
    trips = state_data['trips']
    match message.text:
        case 'Return':
            await to_menu_bar(message, state)
        case _:
            if await check_validation_number_of_trip(len(trips), message.text, message):
                selected_trip = trips[int(message.text) - 1]
                await message.answer(selected_trip.get_info())
                await state.update_data(trip=selected_trip)
                await to_selected_trip_bar(message, state)


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
    match message.text:
        case 'Yes':
            state_data = await state.get_data()
            trip = state_data['trip']
            trip = TripRead.model_validate(trip)
            id = trip.id
            await delete_trip_by_id(id, session)
            await message.answer("Trip deleted successfully")
            await to_planned_trip_bar(message, session, state)
        case 'No':
            await message.answer("Deletion canceled")
            await to_selected_trip_bar(message, state)

@router.message(TripMenu.mark_traveled)
async def command_mark_travelled(message: Message, session: AsyncSession, state: FSMContext):
    match message.text:
        case 'Yes':
            state_data = await state.get_data()
            trip = state_data['trip']
            trip = TripRead.model_validate(trip)
            if (trip.isEnded):
                trip.isEnded = False
                await update_trip_by_id(trip.id, trip, session)
                await message.answer("Trip unmarked as traveled")
                await to_planned_trip_bar(message, session, state)
            else:
                trip.isEnded = True
                await update_trip_by_id(trip.id, trip, session)
                await message.answer("Trip marked as traveled")
                await to_planned_trip_bar(message, session, state)
        case 'No':
            await message.answer("Marking canceled")
            await to_selected_trip_bar(message, state)

