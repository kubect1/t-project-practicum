from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
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

rmk = ReplyKeyboardRemove()

selection_notification_time = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='10 minutes'),
            KeyboardButton(text='20 minutes'),
            KeyboardButton(text='30 minutes'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="select a notification time"
)