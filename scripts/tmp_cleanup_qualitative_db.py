from sqlalchemy import text

from ca_biositing.datamodels.database import get_engine

engine = get_engine()
with engine.begin() as conn:
    conn.execute(text("delete from data_source where id = 5"))
    renames = {
        1: 'stockpile',
        2: 'extractives',
        3: 'human fiber additive',
        4: 'soil amendment',
        5: 'onsite compined heat and power (chp)',
        6: 'compost',
        7: 'animal feed',
        8: 'animal feed',
        9: 'extractives',
        10: 'land application',
        11: 'onsite compined heat and power (chp)',
        12: 'secondary oil extraction',
        13: 'compost',
        14: 'extractives',
        15: 'landfill',
    }
    for use_case_id, new_name in renames.items():
        conn.execute(text("update use_case set name = :name where id = :id"), {"name": new_name, "id": use_case_id})
    conn.execute(text("delete from use_case where id in (22, 23, 24, 25, 26, 27)"))
print('qualitative cleanup complete')
