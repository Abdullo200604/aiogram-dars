import asyncio
import json
import logging
import sys

from aiogram import Bot, Dispatcher, F
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
    # Oddiy tugma: "🛒 Karzinka"
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🛒 Karzinka")]],
        resize_keyboard=True,
        input_field_placeholder="Bo'limni tanlang"
    )

    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!",
        reply_markup=reply_keyboard
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
    await callback.message.answer(f"{product.capitalize()} tanlandi ✅")
    await callback.answer()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
