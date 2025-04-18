import asyncio
import json
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)

from config import TOKEN

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # JSONdan foydalanuvchilarni o‘qish
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)

    # Oddiy tugmalar (foydalanuvchi ismlari va salom)
    name_buttons = [KeyboardButton(text=user['name']) for user in users.values()]
    salom_button = KeyboardButton(text="salom")

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[name_buttons, [salom_button]],
        resize_keyboard=True,
        input_field_placeholder="Tugmalardan birini tanlang"
    )

    # Inline tugma
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="qonday", callback_data="qonday")]
        ]
    )

    # Ikkala keyboardni yuborish
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=reply_keyboard
    )

    await message.answer(
        "Quyidagi tugmani ham bosib ko‘r 👇",
        reply_markup=inline_kb
    )


@dp.message(F.text.isdigit())
async def get_user(message: Message):
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)

    if message.text in users:
        user = users[message.text]
        answer = f"Ismi : {user['name']}, yoshi : {user['age']}"
        await message.answer(answer)
    else:
        await message.answer(f"{message.text} id li user yo'q")


@dp.message()
async def echo_handler(message: Message) -> None:
    if "salom" in message.text.lower():
        await message.answer("Va alaykum assalom")
    else:
        await message.answer(message.text)


@dp.callback_query(F.data == "qonday")
async def handle_qonday(callback: CallbackQuery):
    await callback.message.answer("Buviniki")
    await callback.answer()  # Callbackga javob berish majburiy


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
