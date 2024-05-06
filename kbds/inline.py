from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData



def get_callback_url_btns(
        *,
        btns: dict[str,str],
        sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=data))
    return keyboard.adjust(*sizes).as_markup()

def go_to_privat_btns(
        url: str,
        chat_id= int):
    sizes = (1,)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Начать', url=f'https://t.me/{url}?start=start_{chat_id}'))
    return keyboard.adjust(*sizes).as_markup()

def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():

        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_start_menu_kbds():
    keyboard = InlineKeyboardBuilder()
    sizes = (2,)
    btns = {
        'Мои': 'my',
        'Моей половинки': 'not_my'
    }
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_category_kbds():
    keyboard = InlineKeyboardBuilder()
    btns= {'Хотелки':'desire',
            'Дела и планы':'plan',
            'Меню на покушать':'eat_menu',
            'Шаг назад':'back'}            
    sizes=(3, 1)
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()

def get_desire_kbds():
    keyboard = InlineKeyboardBuilder()
    btns= {'Вкусняшки':'snacks',
            'Сходить / Съездить':'to_go',
            'Купить':'pay',
            'Получить (Вещь, действие)': 'get_thing',
            'Выполнить действие': 'action',
            'Шаг назад': 'back'}
    sizes=(1, 2, 2, 1)
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()

def get_plan_kbds():
    keyboard = InlineKeyboardBuilder()
    btns = {'Сегодня': 'today',
            'На неделю': 'weak',
            'На месяц': 'month',
            'На год': 'yeard',
            'Шаг назад': 'back'}
    sizes=(1, 3, 1)
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()       

def get_eat_menu_kbds():
    keyboard = InlineKeyboardBuilder()
    btns = {'Хочу приготовить':'cook',
            'Хочу покушать':'eat',
            'Шаг назад':'back'}
    sizes=(2, 1)
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()   

def delete_kbds(records):
    keyboard = InlineKeyboardBuilder()
    sizes = (2,)
    for record in records:
        keyboard.add(InlineKeyboardButton(text=record.value, callback_data=str(record.id)))
    return keyboard.adjust(*sizes).as_markup()



