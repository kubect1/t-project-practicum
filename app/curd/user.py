from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserBase


async def create_user(new_user: UserBase, session: AsyncSession) -> User:
    created_user_data = new_user.model_dump(exclude_none=True, exclude_unset=True)
    created_user = await session.execute(
        insert(User).values(**created_user_data).returning(User)
    )
    created_user = created_user.scalars().first()
    await session.commit()
    await session.refresh(created_user)
    return created_user

async def get_user_by_chat_id(chat_id: int, session: AsyncSession) -> User:
    user_by_id = await session.execute(select(User).where(User.chat_id == chat_id))
    user_by_id = user_by_id.scalars().first()
    return user_by_id

async def update_user_by_chat_id(
    user_chat_id: int, user_in: UserBase, session: AsyncSession
) -> User:
    updated_user_data = user_in.model_dump(exclude_none=True, exclude_unset=True)
    updated_user = await session.execute(
        update(User)
        .values(**updated_user_data)
        .where(User.id == user_chat_id)
        .returning(User)
    )
    updated_user = updated_user.scalars().first()
    await session.commit()
    await session.refresh(updated_user)
    return updated_user


async def delete_user_by_chat_id(user_chat_id: int, session: AsyncSession):
    await session.execute(delete(User).where(User.chat_id == user_chat_id))
