from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import traceback

from . import database
from entity import SessionLocal

from database import DuplicateUsernameException, InvalidCredentialsException, UnknownUUIDException
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/user')
async def create_user(name:str, username:str, password:str, session:Session=Depends(get_db)):
    return database.create_user(session, name, username, password)

@app.delete('/user')
def delete_user(username:str, password:str, session:Session=Depends(get_db)):
    database.delete_user(session, username, password)

@app.get('/post')
def get_post(post_uuid:str, session:Session=Depends(get_db)):
    return database.get_post(session, post_uuid)

@app.post('/post')
async def create_post(username:str, password:str, title:str, content:str, session:Session=Depends(get_db)):
    database.create_post(session, username, password, title, content)

@app.put('/post')
def update_post(username:str, password:str, post_uuid:str, title:str, content:str, session:Session=Depends(get_db)):
    database.update_post(session, username, password, post_uuid, title, content)

@app.delete('/post')
def delete_post(username:str, password:str, post_uuid:str, session:Session=Depends(get_db)):
    database.delete_post(session, username, password, post_uuid)

@app.get('/posts/{username}')
def get_posts_by_author(username:str, session:Session=Depends(get_db)):
    return database.get_posts_by_author(session, username)

@app.get('/comment')
def get_comment(comment_uuid:str, session:Session=Depends(get_db)):
    return database.get_comment(session, comment_uuid)

@app.post('/comment')
async def create_comment(username:str, password:str, content:str, session:Session=Depends(get_db)):
    database.create_comment(session, username, password, content)

@app.put('/comment')
def update_comment(username:str, password:str, content:str, session:Session=Depends(get_db)):
    database.update_comment(session, username, password, content)

@app.delete('/comment')
def delete_comment(username:str, password:str, comment_uuid:str, session:Session=Depends(get_db)):
    database.delete_comment(session, username, password, comment_uuid)

@app.get('/comments/{post_uuid}')
def get_comments_by_post(post_uuid:str, session:Session=Depends(get_db)):
    return database.get_comments_by_post(session, post_uuid)

@app.get('/comments/{username}/received')
def get_comments_by_post_author(username:str, session=Depends(get_db)):
    return database.get_comments_by_post_author(session, username)

@app.exception_handler(SQLAlchemyError)
async def handle_database_error(request, exc):
    print(traceback.format_exception(exc))
    return PlainTextResponse('Internal Server Error. Check server log', status_code=500)

@app.exception_handler(DuplicateUsernameException)
async def handle_duplicate_username(request, exc):
    return PlainTextResponse('Duplicate Username Received. Please Try Different Name', status_code=400)

@app.exception_handler(InvalidCredentialsException)
async def handle_invalid_account_info(request, exc):
    return PlainTextResponse('', status_code=400)

@app.exception_handler(UnknownUUIDException)
async def handle_unknown_uuid(request, exc):
    return PlainTextResponse(f'Unknown UUID: {exc.uuid}', status_code=400)
