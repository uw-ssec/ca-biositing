import pandas as pd

def get_geoid(val, county_to_geoid):
    """
    Lookup GEIOD for a given county name or string.
    """
    if pd.isna(val) or not val:
        return "06000"
    val_clean = str(val).strip().lower()
    if val_clean in county_to_geoid:
        return county_to_geoid[val_clean]
    if f"{val_clean} county" in county_to_geoid:
        return county_to_geoid[f"{val_clean} county"]
    return "06000"
