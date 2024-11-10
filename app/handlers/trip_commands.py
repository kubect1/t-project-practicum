from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext


from app.keyboards.builders import reply_builder
from app.keyboards.reply import rmk, selection_notification_time

from app.curd.trip import create_trip, update_trip_by_id, delete_trip_by_id
from app.schemas.trip import TransportEnum, TripBase, TripRead, Coordinates

from app.utils.state import PlanTrip, TripMenu, MainMenu, ChangeTrip
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
                to_place=Coordinates(latitude='', longitude=''),
                from_place=Coordinates(latitude='', longitude=''),
                create_date=message.date.replace(tzinfo=None),
                isEnded=False,
                **trip_data
            ),
            session=session
        )
        if created_trip is None:
            await message.answer("It is impossible to create trip")
        else:
            await message.answer(TripRead.model_validate(created_trip).get_info())
            await message.answer("The trip was saved")
        await to_menu_bar(message, state)



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


async def save_change_trip(trip: TripBase, message: Message, session: AsyncSession, state: FSMContext):
    new_trip = await update_trip_by_id(trip.id, trip, session)
    if new_trip:
        await message.answer('Trip changed successfully')
        await message.answer(TripRead.model_validate(new_trip).get_info())
    else:
        await message.answer("It is impossible to change trip")
    await to_menu_bar(message, state)

@router.message(ChangeTrip.from_place_title)
async def command_change_from_place_title(message: Message, session: AsyncSession, state: FSMContext):
    if await check_validation_string(message.text, message):
        state_data = await state.get_data()
        trip = state_data['trip']
        trip.from_place_title = message.text
        await save_change_trip(trip,message, session, state)


@router.message(ChangeTrip.to_place_title)
async def command_change_to_place_title(message: Message, session: AsyncSession, state: FSMContext):
    if await check_validation_string(message.text, message):
        state_data = await state.get_data()
        trip = state_data['trip']
        trip.to_place_title = message.text
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

