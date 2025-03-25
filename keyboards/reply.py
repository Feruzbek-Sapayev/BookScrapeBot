from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


main_markup_admin = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text="📚 Kitoblar ro'yxati")],
    [KeyboardButton(text="👥 Foydalanuvchilar ro'yxati")],
])


main_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text="📚 Kitoblar ro'yxati")],
])

