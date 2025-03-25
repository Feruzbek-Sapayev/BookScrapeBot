from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


def get_book_btns(l, r, limit):
    book_buttons = InlineKeyboardMarkup(inline_keyboard=[])
    index = l
    btns = []
    while index < r:
        btns.append(InlineKeyboardButton(text=f'{index + 1}', callback_data=f'{index + 1}'))
        index += 1
        if index % 5 == 0:
            book_buttons.inline_keyboard.append(btns)
            btns = []
    print(index)
    if len(btns)!=0:
        print(11111)
        book_buttons.inline_keyboard.append(btns)
    if l == 0 and limit/r>1:
        book_buttons.inline_keyboard.append(
            [InlineKeyboardButton(text=f'➡️', callback_data='next')]
        )
    elif r == limit and l != 0:
        book_buttons.inline_keyboard.append(
            [InlineKeyboardButton(text=f'⬅️', callback_data='previous')]
        )
    elif l==0 and r==limit:
        pass
    else:
        book_buttons.inline_keyboard.append(
            [InlineKeyboardButton(text=f'⬅️', callback_data='previous'), InlineKeyboardButton(text=f'➡️', callback_data='next')]
        )
    return book_buttons


def get_user_btns(n):
    book_buttons = InlineKeyboardMarkup(inline_keyboard=[])
    index = 1
    btns = []
    while index <= n:
        btns.append(InlineKeyboardButton(text=f'{index}', callback_data=f'user_{index}'))
        index += 1
        if index % 5 == 0:
            book_buttons.inline_keyboard.append(btns)
            btns = []
    if len(btns)!=0:
        book_buttons.inline_keyboard.append(btns)
    return book_buttons