# CA Biositing Pipeline

ETL pipeline for the
[CA Biositing](https://github.com/sustainability-software-lab/ca-biositing)
project — extracting biomass feedstock data from Google Sheets and external
sources, transforming it with pandas, and loading it into PostgreSQL.

Workflows are orchestrated with [Prefect](https://www.prefect.io/) and share
database models from the companion
[`ca-biositing-datamodels`](https://pypi.org/project/ca-biositing-datamodels/)
package.

## Installation

```bash
pip install ca-biositing-pipeline
```

## Quick Start

```python
from ca_biositing.pipeline.flows.primary_ag_product import primary_ag_product_flow

# Run the primary agricultural product ETL flow
primary_ag_product_flow()
```

## What's Included

- **Extract** — Pull data from Google Sheets, shapefiles, and public datasets
  (USDA Census/Survey, LandIQ, Billion Ton)
- **Transform** — Clean and reshape with pandas and pyjanitor
- **Load** — Upsert into PostgreSQL with foreign-key resolution
- **Flows** — Prefect flows combining extract/transform/load steps

## Key Dependencies

- [`ca-biositing-datamodels`](https://pypi.org/project/ca-biositing-datamodels/)
  — shared database models
- [Prefect](https://www.prefect.io/) — workflow orchestration
- [pandas](https://pandas.pydata.org/) — data manipulation
- [gspread](https://docs.gspread.org/) — Google Sheets integration
- [GeoPandas](https://geopandas.org/) — geospatial data handling

## Links

- [Repository](https://github.com/sustainability-software-lab/ca-biositing)
- [Issue Tracker](https://github.com/sustainability-software-lab/ca-biositing/issues)

## Contributors

[![Contributors](https://contrib.rocks/image?repo=sustainability-software-lab/ca-biositing)](https://github.com/sustainability-software-lab/ca-biositing/graphs/contributors)

## Acknowledgement

We acknowledge software engineering support from the University of Washington
[Scientific Software Engineering Center (SSEC)](https://escience.washington.edu/software-engineering/ssec/),
as part of the Schmidt Sciences
[Virtual Institute for Scientific Software (VISS)](https://www.schmidtsciences.org/).

## License

CA Biositing Pipeline is licensed under the open source
[BSD 3-Clause License](https://opensource.org/license/bsd-3-clause).
