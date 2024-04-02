from datetime import datetime
from itertools import chain
from uuid import uuid4

from .dto import User as UserDTO
from .dto import Post as PostDTO
from .dto import Comment as CommentDTO
from .dto import PostList, CommentList
from .entity import User, Post, Comment

from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

def verify_user(session:Session, username:str, password:str):
    user = session.scalars(select(User).where(User.username == username)).first()

    if not user or user.password != password: # 실제로는 이러면 안됨
        raise InvalidCredentialsException()
    else:
        return user

def get_post(session:Session, post_uuid:str):
    post = session.scalars(select(Post).where(Post.uuid == post_uuid)).first()

    if not post:
        raise UnknownContentException()
    else:
        return post

def get_comment(session:Session, comment_uuid:str):
    comment = session.scalars(select(Comment).where(Comment.uuid == comment_uuid)).first()

    if not comment:
        raise UnknownContentException()
    else:
        return comment

def create_user(session:Session, name:str, username:str, password:str):
    user = session.scalars(select(User).where(User.username == username)).first()

    if user:
        raise DuplicateUsernameException() # 중복 아이디
    else:
        new_user = User(name=name, username=username, password=password) # 실제로는 이러면 안됨
        execute_transaction(session, lambda: session.add(new_user))

    return UserDTO(name=name, username=username)

def create_post(session:Session, username:str, password:str, title:str, content:str):
    user = verify_user(session, username, password)        
    new_post = Post(uuid=uuid4(), user_id=user.id, title=title, content=content)
    execute_transaction(session, lambda: session.add(new_post))

    return PostDTO(uuid=new_post.uuid, author_name=user.name, title=title, content=content, edited=False, create_time=new_post.create_time)


def create_comment(session:Session, username:str, password:str, post_uuid:str, content:str):
    user = verify_user(session, username, password)
    post = session.scalars(select(Post).where(Post.uuid == post_uuid)).first()

    if not post: # 없는 포스트
        raise UnknownContentException()
    else:
        new_comment = Comment(uuid=uuid4(), user_id=user.id, post_id=post.id, content=content)
        execute_transaction(session, lambda: session.add(new_comment))
    return CommentDTO(uuid=new_comment.uuid, author_name=user.name, is_post_author=post.user_id == user.id, content=content, create_time=new_comment.create_time)

def delete_user(session:Session, username:str, password:str):
    user = verify_user(session, username, password)
    execute_transaction(session, lambda: session.delete(user))

def delete_post(session:Session, username:str, password:str, post_uuid:str):
    user = verify_user(session, username, password)
    post = get_post(session, post_uuid)

    if user.id != post.user_id:
        raise InvalidCredentialsException()
    else:
        execute_transaction(session, lambda: session.delete(post))

def delete_comment(session:Session, username:str, password:str, comment_uuid:str):
    user = verify_user(session, username, password)
    comment = get_comment(session, comment_uuid)

    if user.id != comment.user_id:
        raise InvalidCredentialsException()
    else:
        execute_transaction(session, lambda: session.delete(comment))

def update_post(session:Session, username:str, password:str, post_uuid:str, title:str, content:str):
    user = verify_user(session, username, password)
    post = get_post(session, post_uuid)

    if user.id != post.user_id:
        raise InvalidCredentialsException()
    else:

        def set_post():
            post.title = title
            post.content = content

        execute_transaction(session, lambda: set_post())

def update_comment(session:Session, username:str, password:str, comment_uuid:str, content:str):
    user = verify_user(session, username, password)
    comment = get_comment(session, comment_uuid)

    if user.id != comment.user_id:
        raise InvalidCredentialsException()
    else:

        def set_comment():
            comment.content = content

        execute_transaction(session, lambda: set_comment())

def get_comments_by_post(session:Session, post_uuid:str):
    post = get_post(session, post_uuid)
    return CommentList(comments=[
        CommentDTO(
            uuid=comment.uuid,
            author_name=comment.author.name,
            is_post_author=comment.author.username==post.author.username,
            content=comment.content,
            create_time=comment.create_time
        ) for comment in post.comments
    ])

def get_posts_by_author(session:Session, username:str):
    user = session.scalars(select(User).where(User.username == username)).first()
    return PostList(posts=[
        PostDTO(
            uuid=post.uuid,
            author_name=user.name,
            title=post.title,
            content=post.content
        ) for post in user.posts
    ])

def get_comments_by_post_author(username:str):
    user = session.scalars(select(User).where(User.username == username)).first()

    return CommentList(comments=[
        CommentDTO(
            uuid=comment.uuid,
            author_name=comment.author.name,
            is_post_author=user.id == comment.user_id,
            content=comment.content,
            create_time=comment.create_time
        ) for comment in chain.from_iterable([post.comments for post in user.posts])
    ])
    
def get_comment_by_author(username:str):
    user = session.scalars(select(User).where(User.username == username)).first()

    return CommentList(comments=[
        CommentDTO(
            uuid=comment.uuid,
            author_name=comment.author.name,
            is_post_author=user.id == comment.user_id,
            content=comment.content,
            create_time=comment.create_time
        ) for comment in user.comments
    ])

def execute_transaction(session, stmt_func):
    try:
        stmt_func()
        session.flush()
    except:
        session.rollback()
        raise
    else:
        session.commit()

class DuplicateUsernameException(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass

class UnknownContentException(Exception):
    pass
