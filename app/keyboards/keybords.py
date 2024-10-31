from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='plan a trip'),
            KeyboardButton(text='display all planned trips')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='select an action from the menu'
)