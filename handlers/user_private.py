from aiogram import types, Router, F
from aiogram.filters import CommandStart, StateFilter, or_f
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from filters.chat_types import ChatTypeFilter
from database.orm_query import  orm_get, orm_add, orm_get_all, orm_update, orm_delete
from kbds.inline import delete_kbds, get_callback_btns, get_category_kbds, get_desire_kbds, get_eat_menu_kbds, get_plan_kbds, get_start_menu_kbds

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))
user_private_router.edited_message.filter(ChatTypeFilter(['private']))


class AddIvent(StatesGroup):
    group_chat_id = State()
    choose_user = State()
    choose_category = State()
    choose_sub_category = State()
    choose_action = State()
    value = State()
    delete_value = State()
    choose_record = State()

wish ={
    'desire': 'хотелки',
    'plan': 'дела и планы',
    'eat_menu':'меню на покушать',
    'snacks':'Вкусняшки',
    'go_to':'Сходить / Съездить',
    'pay':'купить',
    'get_thing':'Получить (Вещь, действие)',
    'action':'выполнить дейтсвие',
    'today':'сегодня',
    'weak':'На неделю',
    'month':'На месяц',
    'yeard':'На год',
    'eat':'хочу покушать',
    'cook':'хочу покушать',
}


@user_private_router.message(or_f(CommandStart()))  
async def start_cmd( callback:types.CallbackQuery, state: FSMContext, session: AsyncSession):
   
    if (len(callback.text.split('_'))>1):
        await state.update_data(group_chat_id=int(callback.text.split('_')[1])) # -4118368981
    await callback.answer( 'Чьи пожелания хотели бы посмотреть?',
        reply_markup=get_callback_btns(btns={
            'Мои': 'my',
            'Моей половинки': 'not_my'
        }),
    )
    await state.set_state(AddIvent.choose_user)

@user_private_router.callback_query(StateFilter('*'), F.data.startswith('back'))
async def back_handler(callback: types.CallbackQuery, state: FSMContext):
    curent_state = await state.get_state()
    previous = None
    data = await state.get_data()
    
    
    for step in AddIvent.__all_states__:
        if step.state == curent_state:
            if previous.state.split(':')[-1] == 'choose_user':
                await callback.message.edit_text(
                    'Вернулись на шаг назад', 
                    reply_markup=get_start_menu_kbds())
            elif previous.state.split(':')[-1] == 'choose_category':
                await callback.message.edit_text(
                    'Вернулись на шаг назад',
                    reply_markup=get_category_kbds()
                )
            elif previous.state.split(':')[-1] == 'choose_sub_category' and data['choose_category'] == 'desire':
                await callback.message.edit_text(
                    'Вернулись на шаг назад',
                    reply_markup=get_desire_kbds()
                )
            elif previous.state.split(':')[-1] == 'choose_sub_category' and data['choose_category'] == 'plan':
                await callback.message.edit_text(
                    'Вернулись на шаг назад',
                    reply_markup=get_plan_kbds()
                )
            elif previous.state.split(':')[-1] == 'choose_sub_category' and data['choose_category'] == 'eat_menu':
                await callback.message.edit_text(
                    'Вернулись на шаг назад',
                    reply_markup=get_eat_menu_kbds()
                )
            await state.set_state(previous)
            
            return
        previous = step
    

   


@user_private_router.callback_query(AddIvent.choose_user, F.data.startswith('my'))    
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(choose_user=callback.data)
    await callback.message.edit_text('Выбирите интересующий вас пункт',
        reply_markup=get_callback_btns(btns={
            'Хотелки':'desire',
            'Дела и планы':'plan',
            'Меню на покушать':'eat_menu',
            'Шаг назад':'back'},            
            sizes=(3, 1)
            ),
    )
    await state.set_state(AddIvent.choose_category)


@user_private_router.callback_query(AddIvent.choose_user, F.data.startswith('not_my')) 
async def viewing(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(choose_user=callback.data)
    await callback.message.edit_text('Выберите интересующий вас пункт',
                                     reply_markup=get_callback_btns(
                                         btns={
                                             'Посмотреть все':'get_all',
                                             'Шаг назад':'back'
                                         }
                                     ))
    await state.set_state(AddIvent.choose_category)
    
    

@user_private_router.callback_query(AddIvent.choose_category, F.data.startswith('desire'))
async def choose_desire(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(choose_category=callback.data)
    await callback.message.edit_text(
        'Выберите интересующую вас категорию',
        reply_markup=get_callback_btns(btns={
            'Вкусняшки':'snacks',
            'Сходить / Съездить':'to_go',
            'Купить':'pay',
            'Получить (Вещь, действие)': 'get_thing',
            'Выполнить действие': 'action',
            'Шаг назад': 'back'},
            sizes=(1, 2, 2, 1)
            ),
    )
    await state.set_state(AddIvent.choose_sub_category)

@user_private_router.callback_query(AddIvent.choose_category, F.data.startswith('plan'))
async def choose_plan(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(choose_category=callback.data)
    await callback.message.edit_text(
        'Выберите интересующий вас временной промежуток',
        reply_markup=get_callback_btns(btns={
            'Сегодня': 'today',
            'На неделю': 'weak',
            'На месяц': 'month',
            'На год': 'yeard',
            'Шаг назад': 'back'},
            sizes=(1, 3, 1)
            ),
    )
    await state.set_state(AddIvent.choose_sub_category)

@user_private_router.callback_query(AddIvent.choose_category,  F.data.startswith('eat_menu'))
async def choose_menu_eat(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(choose_category=callback.data)
    await callback.message.edit_text(
        'Выберите хотели бы покушать или самостоятельно приготовить?',
        reply_markup=get_callback_btns(btns={
            'Хочу приготовить':'cook',
            'Хочу покушать':'eat',
            'Шаг назад':'back'},
            sizes=(2, 1)
            ),
    )
    await state.set_state(AddIvent.choose_sub_category)

@user_private_router.callback_query(AddIvent.choose_sub_category)
async def snacke(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(choose_sub_category=callback.data)
    data = await state.get_data()
    if data['choose_user'] == 'my':
        await callback.message.edit_text(
            'Что хотели бы с делать?',
            reply_markup=get_callback_btns(btns={
                'Просмотреть все свои':'get_all',
                'Добавить':'add',
                'Изменить':'choose',
                'Удалить':'delete',
                'Назад':'back'
            },
            sizes=(2,2,1)
            )
        )
    else:
        await callback.message.edit_text(
            'Что хотели бы с делать?',
            reply_markup=get_callback_btns(btns={
                'Просмотреть все':'get_all',
                'Назад':'back'
            }
            )
        )

    await state.set_state(AddIvent.choose_action)


# Вывод списка существующих записей
@user_private_router.callback_query(AddIvent.choose_action, F.data.startswith('get_all'))
async def get_record(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.update_data(choose_action=callback.data)
    data = await state.get_data()
    user_id = callback.from_user.id
    chat_id = data['group_chat_id']
    records = await orm_get(session,  data, user_id, chat_id)
    list_record = [f'{record.value}, создана {str(record.created).split()[0]}' for record in records]
    str_record = '\n'.join(list_record)
    await callback.message.edit_text( f'Вот список: {str_record}')
    await callback.message.answer('Чьи записи хотите посмотреть?',
        reply_markup=get_callback_btns(btns={
            'Мои': 'my',
            'Моей половинки': 'not_my'
        }),
    )
    await state.set_state(AddIvent.choose_user)


# Вывод всех записей партнера    
@user_private_router.callback_query(AddIvent.choose_category, F.data.startswith('get_all'))
async def get_all(callback:types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.update_data(choose_category=callback.data)
    data = await state.get_data()
    user_id = callback.from_user.id
    chat_id = data['group_chat_id']
    records = await orm_get_all(session, data, user_id, chat_id)
    list_record = [f'Категория: {wish[record.category]}, подкатегория: {wish[record.sub_category]} - {record.value}, создана {str(record.created).split()[0]}' for record in records]
    str_record = '\n'.join(list_record) 
    await callback.message.edit_text( f'Вот список: {str_record}')
    await callback.message.answer('Чьи записи вы хотите посмотреть?',
        reply_markup=get_callback_btns(btns={
            'Мои': 'my',
            'Моей половинки': 'not_my'
        }),
    )
    await state.set_state(AddIvent.choose_user)   

# Ввод данных для добавления или изменения
@user_private_router.callback_query(AddIvent.choose_action, F.data.startswith('add'))
async def inter_value(message: types.Message, session: AsyncSession, state:FSMContext):
    await state.update_data(choose_action='add')
    await message.answer('Введите текс с информацией')
    await state.set_state(AddIvent.value)
    
    


# Непосредственное добаление
@user_private_router.message(AddIvent.value)
async def add_callback(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    user_id = message.from_user.id
    chat_id = data['group_chat_id']    
    if data['choose_action'] == 'add':
        await orm_add(session,  data, user_id, chat_id)
        await message.answer(f'Запись добавлена, "{data['value']}"')
        await message.answer('Чьи желание хотите посмотреть?',
                             reply_markup=get_callback_btns(btns={
            'Мои': 'my',
            'Моей половинки': 'not_my'
        }))
        await state.set_state(AddIvent.choose_user)
    elif data['choose_action'] == 'choose':
        await orm_update(session, data)
        await message.answer('Запись обновлена',
                             reply_markup=get_callback_btns(btns={
            'Мои': 'my',
            'Моей половинки': 'not_my'
        }))
        await state.set_state(AddIvent.choose_user)
    

# Обновление записи
@user_private_router.callback_query(AddIvent.choose_action, F.data.startswith('choose'))
async def update_callback(callback:types.CallbackQuery, session: AsyncSession, state:FSMContext):
    await state.update_data(choose_action=callback.data)
    data = await state.get_data()
    user_id = callback.from_user.id
    chat_id = data['group_chat_id']
    records = await orm_get(session,  data, user_id, chat_id)
    await callback.message.edit_text('Выберите что хотите изменить?',
                                     reply_markup=delete_kbds(records))
    await state.set_state(AddIvent.choose_record)    
    

# Выбор номера записи из списка заипсей для последующего удаления
@user_private_router.callback_query(AddIvent.choose_action, F.data.startswith('delete'))
async def delete_value(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.update_data(choose_action=callback.data)
    data = await state.get_data()
    user_id = callback.from_user.id
    chat_id = data['group_chat_id']
    records = await orm_get(session,  data, user_id, chat_id)
    await callback.message.edit_text('Выберите что хотите удалить?',
                                     reply_markup=delete_kbds(records))
    await state.set_state(AddIvent.choose_record)
        

# Непосредственное удаление   
@user_private_router.callback_query(AddIvent.choose_record)
async def delete_action(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.update_data(delete_action=callback.data)
    id_action = int(callback.data)
    data = await state.get_data()
    if data['choose_action'] == 'delete':
        await orm_delete(session, id_action)
        await callback.message.edit_text('Запись удалена',
                                        reply_markup=get_callback_btns(btns={
                                            'Мои': 'my',
                                            'Моей половинки': 'not_my'
                                            }))
        await state.set_state(AddIvent.choose_user)
    elif data['choose_action'] == 'choose':
        await callback.message.edit_text('Введите текс с информацией')
        await state.set_state(AddIvent.value)

   