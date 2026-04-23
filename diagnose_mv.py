import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import os
import sys

# Ensure we can import from src
sys.path.append(os.path.abspath("src/ca_biositing/datamodels"))

from ca_biositing.datamodels.data_portal_views.mv_biomass_search import mv_biomass_search

# Compile the view expression
compiled = mv_biomass_search.compile(
    dialect=postgresql.dialect(),
    compile_kwargs={"literal_binds": True}
)

print(str(compiled))
