from datetime import datetime
from uuid import uuid4

from .dto import User as UserDTO
from .dto import Post as PostDTO
from .dto import Comment as CommentDTO
from .dto import PostList, CommentList
from .entity import User, Post, Comment, engine

from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

def create_user(name:str, username:str, password:str):
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.username == username)).first()
        if user:
            raise DuplicateUsernameException() # 중복 아이디

        new_user = User(name=name, username=username, password=password) # 실제로는 이러면 안됨
        try:
            session.add(new_user)
            session.flush()
        except:
            session.rollback()
            raise
        else:
            session.commit()

def create_post(username:str, password:str, title:str, content:str):
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.username == username)).first()
        if not user.password == password: # 실제로는 이러면 안됨
            raise InvalidCredentialsException() # 비밀번호 오류
        
        new_post = Post(uuid=uuid4(), user_id=user.id, title=title, content=content)
        try:
            session.add(new_post)
            session.flush()
        except:
            session.rollback()
            raise
        else:
            session.commit()

def create_comment(username:str, password:str, post_uuid:str, content:str):
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.username == username)).first()
        post = session.scalars(select(Post).where(Post.uuid == post_uuid)).first()

        if not user.password == password: # 비밀번호 오류
            raise InvalidCredentialsException()
        elif not post: # 없는 포스트
            raise UnknownContentException()

        new_comment = Comment(uuid=uuid4(), user_id=user.id, post_id=post.id, content=content)
        try:
            session.add(new_comment)
            session.flush()
        except:
            session.rollback()
            raise
        else:
            session.commit()

def delete_user(username:str, password:str):
    pass

def delete_post(username:str, password:str, post_uuid:str):
    pass

def delete_comment(username:str, password:str, comment_uuid:str):
    pass

def update_post(username:str, password:str, post_uuid:str, title:str, content:str):
    pass

def update_comment(username:str, password:str, comment_uuid:str, content:str):
    pass

def get_comments_by_post(post_uuid:str):
    pass

def get_posts_by_author(username:str):
    pass

def get_comments_by_post_author(username:str):
    pass

def get_comment_by_author(username:str):
    pass

class DuplicateUsernameException(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass

class UnknownContentException(Exception):
    pass
