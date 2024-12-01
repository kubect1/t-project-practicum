from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    registration = State()
    menu_bar = State()
    planned_trips_bar = State()

class PlanTrip(StatesGroup):
    from_place_title = State()
    from_place = State()
    to_place_title = State()
    to_place = State()
    travel_date = State()
    notification_before_travel = State()
    transport_type = State()


class ChangeTrip(StatesGroup):
    from_place_title = State()
    to_place_title = State()
    travel_date = State()
    notification_before_travel = State()
    transport_type = State()
    location = State()


class TripMenu(StatesGroup):
    selected_trip_bar = State()
    modify_trip = State()
    delete_trip = State()
    mark_traveled = State()
