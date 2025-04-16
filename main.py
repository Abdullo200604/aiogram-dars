import asyncio
import json
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = '7641467002:AAHGWq1AsIC2FRhHrABio4HR5uesZEa7meM'
ADMIN_ID = 7346730386

dp = Dispatcher()

# Foydalanuvchini data.json ga saqlash funksiyasi
def save_user_to_json(user_data: dict, filename: str = "data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []

    data.append(user_data)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    user = message.from_user
    ismi = user.full_name
    user_id = user.id
    username = user.username or 'yo‘q'

    user_data = {
        "ismi": ismi,
        "user_id": user_id,
        "username": username
    }

    save_user_to_json(user_data)

    print(f"Botga /start yuborgan foydalanuvchi:\n"
          f"Ism: {ismi}\n"
          f"Username: @{username}\n"
          f"ID: {user_id}")

    await message.answer(
        f"Salom {ismi}!\n"
        f"Sizning ma'lumotlaringiz:\n"
        f"Ism: {ismi}\n"
        f"Username: @{username}\n"
        f"ID: {user_id}"
    )

    await message.bot.send_message(
        ADMIN_ID,
        f"Yangi foydalanuvchi botga start bosdi!\n"
        f"Ism: {ismi}\n"
        f"Username: @{username}\n"
        f"ID: {user_id}"
    )


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
