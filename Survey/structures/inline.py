from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional, List


class Messenger(CallbackData, prefix='msg'):
    key: Optional[str]
    value: Optional[str]
    action: Optional[str]

async def create_survey(values: List[str],
                        key: Optional[str] = None,
                        action: Optional[str] = None):
    """takes values and crates an inline options from them, key and action = optional param that would be used in Messanger"""
    kb = InlineKeyboardBuilder()
    for value in values:
        kb.button(text=value,
                  callback_data=Messenger(
                      key=key,
                      value=value,
                      action=action
                  ))
    kb.adjust(1)
    return kb.as_markup()

