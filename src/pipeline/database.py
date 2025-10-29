from sqlmodel import create_engine, Session
from config import get_settings

DATABASE_URL = get_settings().DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
