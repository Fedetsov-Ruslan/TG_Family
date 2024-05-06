from sqlalchemy import DateTime, String, func, Integer, Text, ForeignKey, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Desire(Base):
    __tablename__='desires'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(150), nullable=False)
    sub_category: Mapped[str] = mapped_column(String(150), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id',ondelete='CASCADE'))

    

class Users(Base):
    __tablename__='users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_chat_id: Mapped[int] = mapped_column(BigInteger())
    user_id: Mapped[int] = mapped_column()
    #access_id: Mapped[int] = mapped_column()

#class UsersDesire(Base):
#    __table__='desire_connect_users'

    
    

    

