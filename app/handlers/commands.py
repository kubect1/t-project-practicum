from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext


from app.curd.user import create_user, update_user_by_chat_id, get_user_by_chat_id
from app.schemas.user import UserBase
from app.utils.state import MainMenu
from app.utils.navigation_states import to_menu_bar, to_registration, to_plan_trip, to_planned_trip_bar

router = Router(name="commands_router")


@router.message(CommandStart())
async def command_start(message: Message, session: AsyncSession, state: FSMContext):

    user = await get_user_by_chat_id(chat_id=message.from_user.id, session=session)
    if user is None:
        await message.answer("Hello, lets go through the registration")
        await to_registration(message, state)

    else:
        await state.set_state(MainMenu.menu_bar)
        await message.answer(f"Hello, {user.name}")
        await to_menu_bar(message, state)



@router.message(MainMenu.registration)
async def command_create_user(message: Message, session: AsyncSession, state: FSMContext):
    created_user = await create_user(
        new_user=UserBase(
            name=message.text,
            chat_id=message.from_user.id,
            registration_date=message.date.replace(tzinfo=None)
        ),
        session=session
    )
    if created_user is None:
        await message.answer("It is impossible to create user")
    else:
        await message.answer(
            f"Hello {created_user.name} from {created_user.chat_id}! Now you are in my local database!"
        )
        await to_menu_bar(message, state)


@router.message(MainMenu.menu_bar)
async def command_choose_action(message: Message, state: FSMContext):
    match message.text:
        case 'plan a trip':
            await to_plan_trip(message, state)
        case 'display all planned trips':
            await to_planned_trip_bar(message, state)
        case _:
            await message.answer('Press the button')


# @router.message(F.text.startswith("Change user:"))
# async def command_update_user_by_id(message: Message, session: AsyncSession):
#     _, user_text_data = message.text.lower().split(":")
#     user_attrs = user_text_data.split(",")
#     user_data = dict()
#
#     for user_attr in user_attrs:
#         key, value = user_attr.split("=")
#         user_data[key] = int(value) if value.isdigit() else value
#
#     user_id = user_data.get("id")
#     if user_id is None:
#         await message.answer("Wrong data")
#         return
#
#     user = await get_user_by_id(user_id=user_id, session=session)
#     if user is None:
#         await message.answer(f"Can't find user with id: {user_id}")
#         return
#
#     data_for_update = UserBase(**user_data)
#
#     updated_user = await update_user_by_id(
#         user_id=user_id,
#         user_in=data_for_update,
#         session=session
#     )
#
#     if updated_user is None:
#         await message.answer("It is impossible to update user")
#         return
#
#     await message.answer(
#         f"I updated user with id: {user_id}"
#     )
#
#     return
