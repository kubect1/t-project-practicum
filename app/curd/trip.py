from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trip import Trip
from app.schemas.trip import TripBase

async def create_trip(new_trip: TripBase, session: AsyncSession) -> Trip:
    created_trip_data = new_trip.model_dump(exclude_none=True, exclude_unset=True)
    created_trip = await session.execute(
        insert(Trip).values(**created_trip_data).returning(Trip)
    )
    created_trip = created_trip.scalars().first()
    await session.commit()
    await session.refresh(created_trip)
    return created_trip

async def get_trip_by_id(trip_id: int, session: AsyncSession) -> Trip:
    trip_by_id = await session.execute(select(Trip).where(Trip.id == trip_id))
    trip_by_id = trip_by_id.scalars().first()
    return trip_by_id

async def get_trips_by_chatid(chat_id: int, session: AsyncSession):
    trip_array = await session.execute(select(Trip).where(Trip.chat_id == chat_id))
    trip_array = trip_array.all()
    return trip_array
 
async def update_trip_by_id(trip_id: int, trip_in: TripBase, session: AsyncSession) -> Trip:
    updated_trip_data = trip_in.model_dump(exclude_none=True, exclude_unset=True)
    updated_trip = await session.execute(
        update(Trip)
        .values(**updated_trip_data)
        .where(Trip.id == trip_id)
        .returning(Trip)
    )
    updated_trip = updated_trip.scalars().first()
    await session.commit()
    await session.refresh(updated_trip)
    return updated_trip


async def delete_trip_by_id(trip_id: int, session: AsyncSession):
    await session.execute(delete(Trip).where(Trip.id == trip_id))
