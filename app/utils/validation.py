from aiogram.types import Message
import datetime as dt
from app.schemas.trip import TransportEnum


async def check_validation_string(string: str, message: Message) -> bool:
    correct_date = True
    if not string.isalpha():
        correct_date = False
        await message.answer("The string must contain only Cyrillic and Latin characters")

    if not (3 <= len(string) <= 128):
        correct_date = False
        await message.answer("The length of the string must be 3 to 128 characters")

    return correct_date


async def check_validation_travel_datetime(date_time: str, message: Message) -> dt.datetime | None:
    try:
        date, time = date_time.split()
        datetime = dt.datetime.fromisoformat(date + 'T' + time)
    except ValueError:
        await message.answer("Incorrect format")
        return
    if datetime <= message.date.replace(tzinfo=None):
        await message.answer("Time in past cannot be specified")
        return
    if datetime > dt.datetime.fromisoformat("2100-01-01"):
        await message.answer("Travel time must be less than 2100 years")
        return
    return datetime.fromisoformat(date + 'T' + time)

async def check_validation_notification_time(time: str, message: Message) -> dt.datetime | None:
    for value in time.split():
        if not value.isdigit():
            await message.answer("Incorrect format")
    days, hours, minutes, seconds = [int(value) for value in time.split()]
    timedelta_value = dt.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    if not (dt.timedelta(seconds=1) <= timedelta_value <= dt.timedelta(days=365)):
        await message.answer("The notification time can be from 1 second to 1 year")
        return
    return dt.datetime.fromisoformat('1970-01-01') + timedelta_value

async def check_validation_transport_type(transport_type: str, message: Message):
    correct_data = False
    for tr_type in list(TransportEnum):
        if TransportEnum(tr_type).name == transport_type:
            correct_data = True
            break
    if not correct_data:
        await message.answer("Press the button")
    return correct_data





