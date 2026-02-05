# Pull Request: Comprehensive Bioeconomy Geospatial & ETL Integration

## 📄 Description

This PR represents a major consolidation of several months of development work,
integrating advanced geospatial analysis tools, a robust ETL pipeline, and a
refined data modeling architecture. It also incorporates recent contributions
for external data extraction.

### Key Components:

1.  **LinkML & SQLAlchemy Data Layer**:
    - Transitioned to LinkML as the source of truth for data models.
    - Implemented automated SQLAlchemy model generation and Alembic migration
      orchestration.
    - Refactored namespace packages for better modularity across `datamodels`,
      `pipeline`, and `webservice`.

2.  **Enhanced ETL Pipeline (Prefect-orchestrated)**:
    - Implemented robust extraction patterns for Google Sheets and Google Drive
      (CSV, GeoJSON, Zip).
    - Developed test notebooks for etl development
    - Created ETL pipelines for three key analysis types extracted from Gsheets
    - Added lineage tracking for data provenance.
    - Integrated LandIQ dataset processing and infrastructure facility records.
    - Resolved complex hang issues related to Docker/Prefect networking on
      macOS.

3.  **Geospatial Analysis Suite**:
    - Integrated PostGIS for spatial database capabilities.
    - Added comprehensive geospatial cleaning and coercion utilities.
    - Included QGIS integration via Pixi for local visualization.
    - Added specialized notebooks for shapefile extraction and coordinate
      transformations.

4.  **Infrastructure & Developer Experience**:
    - Standardized on Pixi for environment management and task orchestration.
    - Refined Docker Compose configurations for database and Prefect worker
      services.
    - **Notebook & Namespace Integration**: Implemented a standardized Jupyter
      workflow using Pixi-managed kernels to handle PEP 420 namespace package
      imports seamlessly.
    - **Analysis ETL Pipelines**: Developed specialized ETL pipelines and
      notebooks for data analysis, including gsheet extraction and geospatial
      processing.
    - Updated pre-commit hooks (including `codespell` and `prettier`) to
      maintain high code quality.

## ✅ Checklist

- [x] I ran `pre-commit run --all-files` and all checks pass
- [x] Tests added/updated where needed
- [x] Docs added/updated if applicable
- [ ] I have linked the issue this PR closes (if any)

## 💡 Type of change

| Type             | Checked? |
| ---------------- | -------- |
| 🐞 Bug fix       | [x]      |
| ✨ New feature   | [x]      |
| 📝 Documentation | [x]      |
| ♻️ Refactor      | [x]      |
| 🛠️ Build/CI      | [x]      |

## 🧪 How to test

1.  **Environment Setup**: Run `pixi install` to build the unified development
    environment.
2.  **Services**: Start the stack with `pixi run start-services`.
3.  **Migrations**: Apply the consolidated migrations with `pixi run migrate`.
4.  **Data Requirement (LandIQ)**: To verify the LandIQ ETL pipeline, you must
    manually download the LandIQ dataset and place it in the expected data
    directory (see `docs/pr/landiq_pipeline_integration.md` for details).
5.  **ETL Verification**: Run `pixi run run-etl` to verify the pipeline
    orchestration.
6.  **Quality**: Run `pixi run pre-commit-all` to verify linting and formatting.

## 📝 Notes to reviewers

This PR consolidates work previously documented in several internal "mini-PR"
documents found in `docs/pr/`. It is intended to bring the upstream repository
fully up to date with the current production-ready state of the California
Biositing project.

Special attention was paid to resolving the PEP 420 namespace package imports to
ensure seamless integration between the three core sub-packages.
