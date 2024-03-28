from pydantic import BaseModel
from typing import List
from datetime import datetime

class User(BaseModel):
    name: str
    username: str

class Post(BaseModel):
    uuid: str
    author_name: str
    title: str
    content: str
    edited: bool
    create_time: datetime

class Comment(BaseModel):
    uuid: str
    author_name: str
    is_post_author: bool
    content: str
    edited: bool
    create_time: datetime

class CommentList(BaseModel):
    comments: List[Comment]

class PostList(BaseModel):
    posts: List[Comment]
