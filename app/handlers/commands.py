from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from app.curd.user import create_user, update_user_by_id, get_user_by_id
from app.schemas.user import UserBase

router = Router(name="commands-router")


@router.message(CommandStart())
async def command_start(message: types.Message, session: AsyncSession):
    await message.answer("Hello World!")


@router.message(Command("create_user"))
async def command_create_user(message: types.Message, session: AsyncSession):
    created_user = await create_user(
        new_user=UserBase(
            name=message.from_user.first_name,
            chat_id=message.from_user.id
        ),
        session=session
    )
    if created_user is None:
        await message.answer("It is impossible to create user")
        return
    
    await message.answer(
        f"Hello {created_user.name} from {created_user.chat_id}! Now you are in my local database!"
    )

    return


@router.message(F.text.startswith("Change user:"))
async def command_update_user_by_id(message: types.Message, session: AsyncSession):
    _, user_text_data = message.text.lower().split(":")
    user_attrs = user_text_data.split(",")
    user_data = dict()

    for user_attr in user_attrs:
        key, value = user_attr.split("=")
        user_data[key] = int(value) if value.isdigit() else value

    user_id = user_data.get("id")
    if user_id is None:
        await message.answer("Wrong data")
        return

    user = await get_user_by_id(user_id=user_id, session=session)
    if user is None:
        await message.answer(f"Can't find user with id: {user_id}")
        return

    data_for_update = UserBase(**user_data)

    updated_user = await update_user_by_id(
        user_id=user_id,
        user_in=data_for_update,
        session=session
    )

    if updated_user is None:
        await message.answer("It is impossible to update user")
        return

    await message.answer(
        f"I updated user with id: {user_id}"
    )

    return
