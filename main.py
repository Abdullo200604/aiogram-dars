import asyncio
import json
import logging
import sys
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from config import TOKEN

def load_savat():
    if not os.path.exists("savat.json"):
        return {}
    with open("savat.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Savatni saqlash
def save_savat(savat):
    with open("savat.json", "w", encoding="utf-8") as f:
        json.dump(savat, f, ensure_ascii=False, indent=4)

dp = Dispatcher()

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

    savat = load_savat()
    if user_id not in savat:
        savat[user_id] = []
    savat[user_id].append(product)
    save_savat(savat)

    await callback.message.answer(f"{product.capitalize()} savatga qo‘shildi ✅")
    await callback.answer()

@dp.message(F.text == "/savat")
async def show_user_savat(message: Message):
    user_id = str(message.from_user.id)
    savat = load_savat()
    items = savat.get(user_id, [])

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
