from aiogram import types, Router, F, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ContentType, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command, StateFilter, or_f
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


#from app import BOTNAME
from filters.chat_types import ChatTypeFilter
from database.orm_query import orm_add_user, orm_get, orm_add, orm_update, orm_delete
from kbds.inline import go_to_privat_btns,delete_kbds, get_callback_btns, get_category_kbds, get_desire_kbds, get_eat_menu_kbds, get_plan_kbds, get_start_menu_kbds


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group']))
user_group_router.edited_message.filter(ChatTypeFilter(['group']))
BOTNAME = 'Fedetsovs_bot'

@user_group_router.message(F.new_chat_member)
async def check_new_user(message: types.Message, session: AsyncSession):
    invited_user = message.new_chat_members[0].id
    who_invited = message.from_user.id
    chat_id = message.chat.id

    await orm_add_user(session, who_invited, chat_id)
    await orm_add_user(session, invited_user, chat_id)
    await message.reply(
        'Добро пожаловать! Чтоб перейти в приватный чат нажмите на кнопку "Начать"',
        reply_markup=go_to_privat_btns(url=BOTNAME, chat_id=chat_id)
    )   


@user_group_router.message(or_f(CommandStart(), F.text.lower() == 'начать'))
async def private(message: types.Message): 
    chat_id = message.chat.id  
    
           
    await message.reply(
        'Добро пожаловать! Чтоб перейти в приватный чат нажмите на кнопку "Начать"',
        reply_markup=go_to_privat_btns(url=BOTNAME,chat_id=chat_id)
    )
    

