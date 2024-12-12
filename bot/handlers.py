from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.lexicon import LEXICON_RU, LESSONS
from bot.keyboards import create_subjects_keyboard
from bot.states import FillScore, FillName
from db.dao import set_student, login_user, add_score, view_score


router = Router()



@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands='login'))
async def login_command(message: Message, state: FSMContext):
    login = await login_user(
        tg_id=message.from_user.id
    )
    if login is None:
        await message.answer(text=LEXICON_RU['not_found'])
    else:
        await message.answer(
            text=f"Тебя зовут {login.as_dict()['first_name']}\n{LEXICON_RU['sucsess_login']}",
                 reply_markup=create_subjects_keyboard())
    await state.set_state(FillScore.subject)


@router.message(Command(commands='register'))
async def register_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/register'])
    await state.set_state(FillName.first_name)


@router.message(Command(commands='enter_scores'))
async def enter_scores_command(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['enter_score'],
        reply_markup=create_subjects_keyboard())
    await state.set_state(FillScore.subject)


@router.message(Command(commands='view_scores'))
async def view_scores_command(message: Message):
    scores = await view_score(
        tg_id=message.from_user.id
    )
    for score in scores:
        await message.answer(
            text=f"У тебя {score['score']} баллов по предмету {score['subject']}")


@router.message(FillName.first_name, F.text)
async def name_given(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer(text=LEXICON_RU['last_name'])
    await state.set_state(FillName.last_name)


@router.message(FillName.last_name, F.text)
async def last_name_given(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    user_data = await state.get_data()
    await message.answer(
        text=f"Твоё имя: {user_data['first_name']}.\n"
             f"Твоя фамилия: {user_data['last_name']}\n",
    )
    user = await set_student(
        tg_id=message.from_user.id,
        first_name=user_data['first_name'],
        last_name=user_data['last_name']
    )
    await state.clear()
    await message.answer(
        text=LEXICON_RU['sucsess'], reply_markup=create_subjects_keyboard())
    await state.set_state(FillScore.subject)


@router.callback_query(FillScore.subject, F.data.in_(LESSONS))
async def subject_fill(callback: CallbackQuery, state: FSMContext):
    selected_lesson = callback.data
    await state.update_data(subject=LESSONS[selected_lesson])
    await callback.message.answer(
        text=f'Вы выбрали {LESSONS[selected_lesson]}\nВведите баллы')
    await state.set_state(FillScore.score)


@router.message(FillScore.score, F.text)
async def score_fill(message: Message, state: FSMContext):
    try:
        if 0 <= int(message.text) < 101:
            await state.update_data(score=int(message.text))
            await message.answer(text=LEXICON_RU['proceed'])
            score_data = await state.get_data()
            score = await add_score(
                tg_id=message.from_user.id,
                subject=score_data['subject'],
                score=score_data['score']
                )
            await state.clear()
        else:
            await message.answer(text=LEXICON_RU['wrong_num'])
    except ValueError:
        await message.answer(text=LEXICON_RU['wrong_num'])
