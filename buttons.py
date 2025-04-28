from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_karzinka_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍎 Olma", callback_data="product_olma")],
            [InlineKeyboardButton(text="🍇 Uzum", callback_data="product_uzum")],
            [InlineKeyboardButton(text="🍉 Tarvuz", callback_data="product_tarvuz")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
        ]
    )

def get_pagination_buttons(page: int, total_pages: int):
    buttons = []

    if page > 1:
        buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"page_{page-1}"))
    if page < total_pages:
        buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"page_{page+1}"))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])
