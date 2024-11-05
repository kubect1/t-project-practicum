from aiogram.types import Message
import datetime as dt
from app.schemas.trip import TransportEnum, TripBase


async def check_validation_trip_exists(trips: tuple, index: int, message: Message) -> bool:
    correct_index = True
    try:
        value = trips[index]
    except ValueError:
        await message.answer("There doesnt exist a trip with that index")
        correct_index = False
    return correct_index
