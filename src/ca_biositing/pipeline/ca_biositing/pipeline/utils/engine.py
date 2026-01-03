from sqlmodel import create_engine, Session

DATABASE_URL = "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"
engine = create_engine(DATABASE_URL)

db_session = Session(engine)
