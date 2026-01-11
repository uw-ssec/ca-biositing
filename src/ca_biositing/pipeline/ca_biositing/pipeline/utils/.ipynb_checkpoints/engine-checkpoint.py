from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

#This module queries the db via the ORM

# Get the root
path = os.getcwd()
project_root = None
while path != os.path.dirname(path): # Stop at the filesystem root
    if 'pixi.toml' in os.listdir(path):
        project_root = path
        break
    path = os.path.dirname(path)

load_dotenv(dotenv_path=project_root + "\\resources\\docker\\.env")

# Database Connection
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD= os.getenv("POSTGRES_PASSWORD")

# 2. Host Port Mapping
# This is the port on your local machine that will connect to the container's port 5432.
POSTGRES_PORT= os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/biocirv_db"

# old:
# DATABASE_URL = "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"
engine = create_engine(DATABASE_URL)

db_session = Session(engine)
