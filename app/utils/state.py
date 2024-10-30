from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    registration = State()
    menu_bar = State()
    plan_trip = State()
    planned_trips_bar = State()


class TripMenu(StatesGroup):
    selected_trip_bar = State()
    modify_trip = State()
    delete_trip = State()
    mark_traveled = State()
