from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.lexicon import LEXICON_RU, LESSONS


def create_subjects_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for key, value in LESSONS.items():
        button = InlineKeyboardButton(text=value, callback_data=key)
        kb_builder.add(button)
        kb_builder.adjust(2)
    return kb_builder.as_markup()


def check_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    yes_button = InlineKeyboardButton(text="✅ Да", callback_data="yes")
    no_button = InlineKeyboardButton(text="❌ Нет", callback_data="no")
    kb_builder.add(yes_button, no_button)
    return kb_builder.as_markup()
