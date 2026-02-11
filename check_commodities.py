import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db')
with engine.connect() as conn:
    # Check usda_commodity table
    result = conn.execute(text('SELECT id, name, api_name FROM usda_commodity ORDER BY id'))
    print('=== USDA_COMMODITY TABLE ===')
    for row in result:
        print(f'{row[0]:3}: name="{row[1]}" api_name="{row[2]}"')

    # Check what data is in census records
    result = conn.execute(text('SELECT DISTINCT commodity_code FROM usda_census_record ORDER BY commodity_code'))
    print('\n=== COMMODITY CODES IN CENSUS RECORDS ===')
    for row in result:
        print(f'  {row[0]}')
