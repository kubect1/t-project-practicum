from aiogram.utils.keyboard import ReplyKeyboardBuilder

def default_builder(text: [str | list]):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    for txt in text:
        builder.button(text=txt)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
