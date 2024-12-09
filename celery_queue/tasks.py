import asyncio

import aiohttp
import redis
import datetime as dt


from app.schemas.trip import TripRead
from app.curd.trip import get_all_trips
from app.core.db import AsyncSessionLocal
from celery import shared_task
from app.core.config import settings

redis_client = redis.from_url(settings.redis_url)
left_border = dt.timedelta(minutes=10)
right_border = dt.timedelta(minutes=40)
last_check_notification = 'last_check_notification'


@shared_task()
async def check_notification_to_send():
    session = AsyncSessionLocal()
    trips = asyncio.run(get_all_trips(session))
    trips = [TripRead.model_validate(trip) for trip in trips]
    current_time = dt.datetime.now(dt.UTC).replace(tzinfo=None)
    redis_client.set(last_check_notification, current_time.isoformat())
    for trip in trips:
        notification_time = (trip.travel_date - (trip.notification_before_travel - dt.datetime.fromisoformat('1970-01-01')))
        if notification_time <= current_time:
            continue
        if left_border <= (notification_time - current_time) <= right_border:
            send_notification_trip.aplay_async(args=[trip], eta=notification_time)


@shared_task()
async def send_notification_trip(trip):
    trip: TripRead = TripRead.model_validate_json(trip)
    url = f'https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage'
    params = {
        'chat_id': trip.chat_id,
        'text': 'You have a scheduled trip with early start time coming up:' + '\n' + trip.get_info()
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as response:
            result = response.json()
    return result


async def get_last_check_notification_time() -> dt.datetime | None:
    last_run_time = redis_client.get(last_check_notification)
    if last_run_time:
        last_run_time = last_run_time.decode('utf-8')
        return dt.datetime.fromisoformat(last_run_time)
    return None




