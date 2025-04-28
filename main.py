import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from config import TOKEN
from buttons import get_karzinka_buttons, get_pagination_buttons

dp = Dispatcher()

products = [f"ustozni maxsulati {i}" for i in range(1, 101)]
Page = 10

@dp.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Korzinka")],
            [KeyboardButton(text="📦 Mahsulotlar")]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!", reply_markup=keyboard)

@dp.message(F.text == "🛒 Korzinka")
async def show_karzinka(message: Message):
    await message.answer("Mahsulotni tanlang:", reply_markup=get_karzinka_buttons())
    await message.answer(reply_markup=ReplyKeyboardRemove())

@dp.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("🏠 Asosiy menyuga qaytdingiz.")

@dp.callback_query(F.data.startswith("product_"))
async def product_selected(callback: CallbackQuery):
    product_name = callback.data.split("_")[1]
    await callback.answer(f"{product_name.capitalize()} tanladingiz!")

@dp.message(F.text == "📦 Mahsulotlar")
async def show_products(message: Message):
    await send_products(message, page=1)

async def send_products(message_or_callback, page: int):
    start = (page - 1) * Page
    end = start + Page
    total_pages = (len(products) + Page - 1) // Page

    text = "\n".join(products[start:end])
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            f"📦 Mahsulotlar (sahifa {page}/{total_pages}):\n\n{text}",
            reply_markup=get_pagination_buttons(page, total_pages)
        )
    else:
        await message_or_callback.message.edit_text(
            f"📦 Mahsulotlar (sahifa {page}/{total_pages}):\n\n{text}",
            reply_markup=get_pagination_buttons(page, total_pages)
        )

@dp.callback_query(F.data.startswith("page_"))
async def pagination(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    await send_products(callback, page)

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
