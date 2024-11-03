from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder

def reply_builder(text: [str | list]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    for txt in text:
        builder.button(text=txt)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def inline_builder(text: [str | list]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    for txt in text:
        builder.button(text=txt)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
