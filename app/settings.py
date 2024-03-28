from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    dbapi_url_file: str

settings = Settings()
dbapi_url = None
with open(dbapi_url_file, 'r') as f:
    dbapi_url = f.read()
