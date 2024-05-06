from sqlalchemy import exists, select, update, delete, values
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Desire, Users


async def orm_get(session: AsyncSession, data: dict, user_id: int, chat_id: int):
    id_query = await session.execute(select(Users.id).where(Users.user_id == user_id, Users.group_chat_id == chat_id))
    query = select(Desire).where(Desire.user_id == id_query.scalar(), Desire.category == data['choose_category'], Desire.sub_category == data['choose_sub_category'])
    result = await session.execute(query)   
    return result.scalars().all()


    

async def orm_update(session: AsyncSession, data: dict):
    query = update(Desire).where(Desire.id == int(data['delete_action'])).values(value=data['value'])
    await session.execute(query)
    await session.commit()


async def orm_add(session: AsyncSession, data: dict, user_id: int, chat_id:int):  
    print(data, user_id, chat_id)
    id_query = await session.execute(select(Users.id).where(Users.user_id == user_id, Users.group_chat_id == chat_id))
    obj = Desire(
        user_id=id_query.scalar(),
        category=data["choose_category"],
        sub_category=data['choose_sub_category'],
        value=data['value'],            
    )
    session.add(obj)
    await session.commit()

    


async def orm_delete(session: AsyncSession, id:int):
    query = delete(Desire).where(Desire.id == id)
    await session.execute(query)
    await session.commit()


async def orm_get_all(session: AsyncSession, data:dict, user_id: int, chat_id: int):
    query = select(Users).where(Users.group_chat_id == chat_id, Users.user_id != user_id)
    result_user = await session.execute(query)
    print(f'dsdsd{result_user}' )
    query = select(Desire).where(Desire.user_id == result_user.scalar().id)
    result = await session.execute(query)
    return result.scalars().all()
    


async def orm_add_user(session: AsyncSession, user_id: int, chat_id:int):
    query = select(Users).where(Users.user_id == user_id, Users.group_chat_id == chat_id)
    result = await session.execute(query)
    if result.scalar():
        #query = update(Users).where(Users.user_id == user_id).values(groupt_chat_id=chat_id)
        #await session.execute(query)
        print('user choose in group')
        return
        #await session.commit()
        
    else:
        obj=Users(
            user_id=user_id,
            group_chat_id=chat_id
        )
        session.add(obj)
        print('user add in group')
        await session.commit()

async def orm_add_chat(session: AsyncSession, user_id:int, group_chat_id: int, chat_id: int ):
    query = update(Users).where(Users.user_id == user_id, Users.group_chat_id == group_chat_id).values(chat_id=chat_id)
    await session.execute(query)
    await session.commit()
