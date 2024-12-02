from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
import datetime as dt


from app.keyboards.builders import reply_builder
from app.keyboards.reply import rmk, selection_notification_time

from app.curd.trip import update_trip_by_id, delete_trip_by_id
from app.schemas.trip import TransportEnum, TripRead
from app.utils.get_timezone import get_timezone, timezone_adaptation
from app.utils.notifiaction import check_need_to_create_task_immediately, cancel_notification

from app.utils.state import TripMenu, MainMenu, ChangeTrip
from app.utils.navigation_states import to_menu_bar, to_modify_trip, to_delete_trip, to_mark_traveled, \
    to_selected_trip_bar, \
    to_planned_trip_bar, to_change_location
from app.utils.validation import check_validation_string, check_validation_travel_datetime, \
    check_validation_transport_type, check_validation_number_of_trip, check_validation_location

from celery_queue.tasks import get_last_check_notification_time, right_border

router = Router(name="trip_commands_router")


@router.message(MainMenu.planned_trips_bar)
async def command_choose_trip(message: Message, state: FSMContext):
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
async def command_choose_action_with_trip(message: Message, state: FSMContext):
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
async def command_modify_trip(message: Message, state: FSMContext):
    match message.text:
        case 'Return':
            await to_selected_trip_bar(message, state)
        case 'from place title':
            await message.answer('Enter new from place title')
            await state.set_state(ChangeTrip.from_place_title)
        case 'to place title':
            await message.answer('Enter new to place title')
            await state.set_state(ChangeTrip.to_place_title)
        case 'travel date':
            await message.answer('Enter new travel date and new time in format: "YYYY-MM-DD HH:MM:SS", without quotation marks',
                                 reply_markup=rmk)
            await state.set_state(ChangeTrip.travel_date)
        case 'notification before travel':
            await message.answer(
                'Enter a new time for notification before travel if format: "days hours minutes seconds", '
                'without quotation marks where you write numbers instead of words',
                reply_markup=selection_notification_time)
            await state.set_state(ChangeTrip.notification_before_travel)
        case 'transport type':
            await message.answer(
                "Choose new type of transport",
                reply_markup=reply_builder(
                    [TransportEnum(transport_type).name for transport_type in list(TransportEnum)])
            )
            await state.set_state(ChangeTrip.transport_type)
        case _:
            await message.answer('Print the button')


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
            if trip.isEnded:
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


async def save_change_trip(trip: TripRead, message: Message, session: AsyncSession, state: FSMContext) -> TripRead | None:
    new_trip = await update_trip_by_id(trip.id, trip, session)
    if new_trip:
        new_trip = TripRead.model_validate(new_trip)
        old_notification_time = (trip.travel_date -
                                 (trip.notification_before_travel - dt.datetime.fromisoformat('1970-01-01')))
        new_notification_time = (new_trip.travel_date -
                                 (new_trip.notification_before_travel - dt.datetime.fromisoformat('1970-01-01')))
        if old_notification_time != new_notification_time:
            last_check_time = get_last_check_notification_time()
            if old_notification_time <= (last_check_time + right_border):
                cancel_notification(trip)
            check_need_to_create_task_immediately(new_trip)
        await message.answer('Trip changed successfully')
        await message.answer(new_trip.get_info())
        return new_trip
    else:
        await message.answer("It is impossible to change trip")
    await to_menu_bar(message, state)

@router.message(ChangeTrip.from_place_title)
async def command_change_from_place_title(message: Message, state: FSMContext):
    if await check_validation_string(message.text, message):
        state_data = await state.get_data()
        trip = state_data['trip']
        trip.from_place_title = message.text
        await state.update_data(trip=trip)
        await state.update_data(type_place='from')
        await to_change_location(message, state)


@router.message(ChangeTrip.to_place_title)
async def command_change_to_place_title(message: Message, state: FSMContext):
    if await check_validation_string(message.text, message):
        state_data = await state.get_data()
        trip = state_data['trip']
        trip.to_place_title = message.text
        await state.update_data(trip=trip)
        await state.update_data(type_place='to')
        await state.set_state(ChangeTrip.location)
        await message.answer('Send the location of the place with an attachment', reply_markup=rmk)


@router.message(ChangeTrip.location)
async def command_change_location(message: Message, session: AsyncSession, state: FSMContext):
    location = await check_validation_location(message)
    if location:
        state_data = await state.get_data()
        trip = state_data['trip']
        type_place = state_data['type_place']
        match type_place:
            case 'to':
                trip.to_place = location
            case 'from':
                trip.from_place = location
                tz = get_timezone(location)
                trip.datetime = timezone_adaptation(trip.datetime, tz)
        await save_change_trip(trip, message, session, state)





@router.message(ChangeTrip.travel_date)
async def command_change_travel_date(message: Message, session: AsyncSession, state: FSMContext):
    datetime = await check_validation_travel_datetime(message.text, message)
    if datetime:
        state_data = await state.get_data()
        trip = state_data['trip']
        trip.travel_date = datetime
        await save_change_trip(trip, message, session, state)


@router.message(ChangeTrip.notification_before_travel)
async def command_change_notification_before_travel(message: Message, session: AsyncSession, state: FSMContext):
    datetime = await check_validation_string(message.text, message)
    if datetime:
        state_data = await state.get_data()
        trip = state_data['trip']
        trip.notification_before_travel = datetime
        await save_change_trip(trip, message, session, state)



@router.message(ChangeTrip.transport_type)
async def command_change_transport_type(message: Message, session: AsyncSession, state: FSMContext):
    if await check_validation_transport_type(message.text, message):
        state_data = await state.get_data()
        trip = state_data['trip']
        trip.transport_type = TransportEnum(getattr(TransportEnum, message.text))
        await save_change_trip(trip, message, session, state)

