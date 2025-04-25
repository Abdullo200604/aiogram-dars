import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from config import TOKEN

dp = Dispatcher()
savatlar = {}

@dp.message(CommandStart())
async def start_menu(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🛒 Karzinka")]],
        resize_keyboard=True
    )
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!",
        reply_markup=keyboard
    )

@dp.message(F.text == "🛒 Karzinka")
async def show_karzinka_inline(message: Message):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍎 Olma", callback_data="olma")],
            [InlineKeyboardButton(text="🍇 Uzum", callback_data="uzum")],
            [InlineKeyboardButton(text="🍉 Tarvuz", callback_data="tarvuz")],
        ]
    )
    await message.answer("Mahsulotni tanlang:", reply_markup=inline_kb)

@dp.callback_query()
async def handle_product_selection(callback: CallbackQuery):
    product = callback.data
    user_id = str(callback.from_user.id)

    if user_id not in savatlar:
        savatlar[user_id] = []
    savatlar[user_id].append(product)

    await callback.message.answer(f"{product.capitalize()} savatga qo‘shildi ✅")
    await callback.answer()

@dp.message(F.text == "/savat")
async def show_user_savat(message: Message):
    user_id = str(message.from_user.id)
    items = savatlar.get(user_id, [])

    if items:
        matn = "🧺 Sizning savatingiz:\n" + "\n".join(f"• {item.capitalize()}" for item in items)
    else:
        matn = "🧺 Sizning savatingiz bo‘sh."
    await message.answer(matn)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
