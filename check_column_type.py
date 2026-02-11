#!/usr/bin/env python3
import os
from sqlalchemy import create_engine, text

db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db')
engine = create_engine(db_url, echo=False)

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'usda_commodity'
        AND column_name = 'usda_code'
    """))
    row = result.fetchone()
    print(f'usda_code column type: {row[1] if row else "Column not found"}')
