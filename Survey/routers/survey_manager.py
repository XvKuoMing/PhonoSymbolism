from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from structures.inline import create_survey, Messenger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from content.utils import gen_brands_names
from content.dialog import DIALOG
from db.queries import save_results

survey_managed = Router()


class Survey(StatesGroup):
    q2 = State()
    q3 = State()


@survey_managed.callback_query(Messenger.filter(F.key == 'Q1'))
async def get_first_q_result(callback: CallbackQuery, callback_data: Messenger, state: FSMContext) -> None:
    user_session = await state.get_data()
    await state.clear()
    await state.set_state(Survey.q2)  # переходим к следующему вопросу
    await state.update_data(firstly_chosen_group=user_session['brands'][callback_data.value])
    await state.update_data(user_id=user_session['user_id'])
    await callback.answer()
    await callback.message.answer(text=DIALOG['Q2'])
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=None)

@survey_managed.message(Survey.q2)
async def save_q2(message: Message, state: FSMContext) -> None:
    await state.set_state(Survey.q3)
    await state.update_data(associations=message.text[:255])
    await message.answer(text=DIALOG['Q3'])

@survey_managed.message(Survey.q3)
async def save_q3(message: Message, state: FSMContext) -> None:
    await state.update_data(image=message.text)
    await message.answer(text=DIALOG['Q4'],
                         reply_markup=await create_survey(
                             key='Q4',
                             values=['да', 'нет']
                         ))

@survey_managed.callback_query(Messenger.filter(F.key == 'Q4'))
async def save_q4(callback: CallbackQuery, callback_data: Messenger, state: FSMContext) -> None:
    await state.update_data(is_interested=callback_data.value)
    await callback.answer()
    brands = await gen_brands_names()
    await state.update_data(brands=brands)
    await callback.message.answer(text=DIALOG['Q5'],
                                  reply_markup=await create_survey(
                                      key='Q5',
                                      values=brands.keys()
                                  ))
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=None)

@survey_managed.callback_query(Messenger.filter(F.key == 'Q5'))
async def save_q5(callback: CallbackQuery, callback_data: Messenger, state: FSMContext) -> None:
    user_session = await state.get_data()
    brands = user_session.pop('brands')
    user_session['lastly_chosen_group'] = brands[callback_data.value]
    await save_results(**user_session)
    await callback.answer()
    await callback.message.answer(text=DIALOG['FINISHED'])
    await state.clear()
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=None)

