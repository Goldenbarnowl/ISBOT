import json

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PollAnswer

from config import bot
from random import shuffle

user_router = Router()

def converter(word):
    if word == "а":
        return 0
    if word == "б":
        return 1
    if word == "в":
        return 2
    if word == "г":
        return 3


async def send_test(chat_id, state, counter):
    data = await state.get_data()
    c = int(data.get("counter"))
    with open("full_questions_141.json", encoding="utf-8") as file:
        questions_test = json.load(file)

    if counter == 80:
        await bot.send_poll(
            chat_id=chat_id,
            question=f"[{c + 1}/141][{counter + 1}]" + questions_test[counter]["question"],
            options=["а) " + questions_test[counter]["а"],
                     "б) " + questions_test[counter]["б"],
                     "в) " + questions_test[counter]["в"],
                     "г) " + questions_test[counter]["г"]],
            is_anonymous=False,
            allows_multiple_answers=True
        )

        return

    if ((len(questions_test[counter]["question"]) >= 300
        or len(questions_test[counter]["а"]) >= 100 or len(questions_test[counter]["б"]) >= 100
            or len(questions_test[counter]["в"]) >= 100 or len(questions_test[counter]["г"]) >= 100)):
        await bot.send_message(
            chat_id=chat_id,
            text=(
                f"<b>{questions_test[counter]["question"]}</b> \n\n\n "
                f"а) {questions_test[counter]['а']} \n\n "
                f"б) {questions_test[counter]['б']} \n\n "
                f"в) {questions_test[counter]['в']} \n\n "
                f"г) {questions_test[counter]['г']}"
                )
        )
        await bot.send_poll(
            chat_id=chat_id,
            type="quiz",
            question=f"[{c+1}/141][{counter+1}]",
            options=["а", "б", "в", "г"],
            correct_option_id=converter(questions_test[counter]["answer"]),
            is_anonymous=False)

        return
    await bot.send_poll(
        chat_id=chat_id,
        type="quiz",
        question=f"[{c+1}/141][{counter+1}]" + questions_test[counter]["question"],
        options=["а) "+questions_test[counter]["а"],
                 "б) "+questions_test[counter]["б"],
                 "в) "+questions_test[counter]["в"],
                 "г) "+questions_test[counter]["г"]],
        correct_option_id=converter(questions_test[counter]["answer"]),
        is_anonymous=False,
    )


@user_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    question_number = list(range(141))
    shuffle(question_number)
    await state.update_data(question_number=question_number)
    counter = 0
    await state.update_data(counter=str(counter))
    await send_test(message.from_user.id, state, question_number[counter])
    counter += 1
    await state.update_data(counter=str(counter))


@user_router.poll_answer()
async def answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    counter = int(data.get("counter"))
    question_number = data.get("question_number")
    if question_number[counter-1] == 80:
        await bot.send_message(
            chat_id=poll_answer.user.id,
            text="Единственный вопрос с двумя ответами А,В"
        )
    await send_test(poll_answer.user.id, state, question_number[counter])
    counter += 1
    await state.update_data(counter=str(counter))


