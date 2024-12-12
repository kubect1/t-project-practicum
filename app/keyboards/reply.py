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

trip_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Change trip'),
            KeyboardButton(text='Delete trip'),
            KeyboardButton(text='Mark as travelled'),
            KeyboardButton(text='Return')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='select an action from the menu'
)

confirm_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Yes'),
            KeyboardButton(text='No'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Confirm or reject'
)

selection_field_for_change = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='from place title'),
            KeyboardButton(text='from place'),

        ],
        [
            KeyboardButton(text='to place title'),
            KeyboardButton(text='to place'),
        ],
        [
            KeyboardButton(text='travel date'),
            KeyboardButton(text='notification before travel'),
        ],
        [
            KeyboardButton(text='transport type'),
            KeyboardButton(text='Return')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='select what you want to change'
)