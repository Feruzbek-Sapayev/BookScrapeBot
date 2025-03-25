import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import db
from api import get_all_books
from keyboards.reply import main_markup, main_markup_admin
from keyboards.inline import get_book_btns, get_user_btns
from states import UserState

TOKEN = "7266604018:AAG5NvX_gZGwZED9OLGcv_tgd3-X-p39Hb0"
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))



@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user = db.select_user(message.from_user.id)
    if not user:
        photos = await bot.get_user_profile_photos(message.from_user.id)
        if photos.total_count > 0:
            photo = photos.photos[0][-1].file_id
        else:
            photo = None
        first_name = message.from_user.first_name  
        telegram_id = message.from_user.id  
        last_name = message.from_user.last_name
        username = message.from_user.username
        db.add_user(first_name, last_name, telegram_id, photo, username)
    if message.from_user.id == 6127805179:
        await message.answer(f"👋 Assalomu aleykum, {html.bold(message.from_user.full_name)}!", reply_markup=main_markup_admin)
    else:
        await message.answer(f"👋 Assalomu aleykum, {html.bold(message.from_user.full_name)}!", reply_markup=main_markup)
    
    
@dp.message(UserState.send_message)
async def send_message_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    user_id = data['user_id']
    await message.send_copy(chat_id=user_id)
    await message.answer("✅ Xabar yuborildi!", reply_markup=main_markup_admin)
    await state.clear()

@dp.message()
async def main_handler(message: Message, state: FSMContext) -> None:
    if message.text and message.text == "📚 Kitoblar ro'yxati":
        books = get_all_books()
        await state.set_data({'page': 0, 'books': books})
        txt = ""
        page = 0
        l = page * 10
        if l + 10 <= len(books):
            r = l + 10
        else:
            r = l + (len(books) - l)
        markup = get_book_btns(l, r, len(books))
        while l < r:
            txt += f"<b>{l+1}.</b> {books[l]['title']}\n"
            l += 1
        await message.answer(txt, reply_markup=markup)
    
    if message.text and message.text == "👥 Foydalanuvchilar ro'yxati":
        users  = db.select_all_users()
        txt = "<b>👥 Foydalanuvchilar ro'yxati:</b>\n\n"
        markup = get_user_btns(len(users))
        for i in range(len(users)):
            txt += f"<b>{i+1}.</b> {users[i][1]} {str(users[i][2]).replace("None", "-")}\n"
        await message.answer(txt, reply_markup=markup)


@dp.callback_query()
async def main_call_back_handler(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        books = data['books']
    except:
        books = []
    if call.data == "next":
        txt = ""
        page = data['page'] + 1
        await state.update_data({'page': page}) 
        if len(books) >= 10 * page:
            l = page * 10
            if l + 10 <= len(books):
                r = l + 10
            else:
                r = l + (len(books) - l)
            markup = get_book_btns(l, r, len(books))
            while l < r:
                txt += f"<b>{l+1}.</b> {books[l]['title']}\n"
                l += 1
        if len(txt)>0:
            await call.message.edit_text(txt, reply_markup=markup)
    
    if call.data == "previous":
        data = await state.get_data()
        txt = ""
        page = data['page'] - 1
        await state.update_data({'page': page}) 
        if len(books) >= 10 * page:
            l = page * 10
            if l + 10 <= len(books):
                r = l + 10
            else:
                r = l + (len(books) - l)
            markup = get_book_btns(l, r, len(books))
            print(l, r)
            while l < r:
                txt += f"<b>{l+1}.</b> {books[l]['title']}\n"
                l += 1
        if len(txt)>0:
            await call.message.edit_text(txt, reply_markup=markup)
        
    if call.data.isdecimal():
        if 1<=int(call.data)<=len(books):
            book = books[int(call.data)-1]
            title = book['title']
            price = f"{book['price']:,}".replace(",", " ") + " so'm"
            photo = book['image']
            description = book['description']
            if len(description)>300:
                description = description[:300] + "..."
            txt = f"<b>{title}</b>\n\n<b>Narxi:</b> {price}\n\n{description}"
            await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=txt)
    
    if call.data.startswith('user_'):
        _, number = call.data.split('_')
        number = int(number)
        users = db.select_all_users()
        user = users[number-1]
        await call.message.answer(f"<b>{user[1]}</b> ga xabar yuborish uchun matn kiriting:")
        await state.set_state(UserState.send_message)
        await state.update_data({'user_id': user[5]})

    await call.answer()




@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())