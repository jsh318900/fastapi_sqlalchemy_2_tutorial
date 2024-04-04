"""Summary
"""
__all__ = ['engine', 'User', 'Post', 'Comment']

from typing import List
from sqlalchemy import MetaData, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from .settings import dbapi_url


metadata = MetaData()
engine = create_engine(dbapi_url, echo=True) # 모든 쿼리를 로그 남기고 싶을 때 echo=True로 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):

    """Summary
    """
    
    pass

class User(Base):

    """Summary
    """
    
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement='auto')
    name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[List['Post']] = relationship(back_populates='author', cascade='all, delete-orphan')
    comments: Mapped[List['Comment']] = relationship(back_populates='author', cascade='all, delete-orphan')

class Post(Base):

    """Summary
    """
    
    __table__ = Table('post', metadata, autoload_with=engine)

    author: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped['Comment'] = relationship(back_populates='post', cascade='all, delete-orphan')

class Comment(Base):

    """Summary
    """
    
    __table__ = Table('comment', metadata, autoload_with=engine)

    author: Mapped['User'] = relationship(back_populates='comments')
    post: Mapped['Post'] = relationship(back_populates='comments')
