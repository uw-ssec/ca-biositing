# Generating SQLAlchemy Models from LinkML Schemas

This document outlines the process of generating SQLAlchemy (SQLA) models from
LinkML schemas and integrating them with Alembic for database migrations.

## 1. Create a LinkML Schema

Create a YAML file (e.g., `my_schema.yaml`) to define your data model. The
schema should include:

- **`id`**: A unique identifier for the schema.
- **`name`**: A human-readable name for the schema.
- **`description`**: A brief description of the schema's purpose.
- **`prefixes`**: A mapping of prefixes to URIs for linked data.
- **`imports`**: A list of other LinkML schemas to import.
- **`classes`**: The main data structures of your model.
- **`slots`**: The properties of your classes.
- **`enums`**: Controlled vocabularies for your slots.

## 2. Define Classes and Slots

Define your classes and their corresponding slots. For SQLAlchemy model
generation, it's important to specify the table name using the `__tablename__`
annotation to ensure snake_case naming conventions.

```yaml
classes:
  MyClassName:
    description: "A description of my class."
    annotations:
      __tablename__: my_snake_case_name
    slots:
      - my_slot_name
```

## 3. Generate SQLAlchemy Models

Use the `linkml-sqla` generator to create SQLAlchemy models from your schema.
The following command will generate a Python file containing your models:

```bash
linkml generate sqla my_schema.yaml > schemas/generated/my_model.py
```

If your schema imports other schemas, you may want to use the
`--no-mergeimports` flag to avoid including the imported models in the generated
file:

```bash
linkml generate sqla --no-mergeimports my_schema.yaml > schemas/generated/my_model.py
```

## 4. Integrate with Alembic

Once you have your generated models, you can use Alembic to create and apply
database migrations.

### a. Configure Alembic

Ensure your `alembic/env.py` is configured to use your generated models. You
will need to explicitly import your generated models and then merge their
metadata with your main `SQLModel` metadata.

```python
# alembic/env.py
import os
import sys
from sqlmodel import SQLModel

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Import your main models
from src.pipeline.etl.models import *

# Import your generated models
from schemas.generated.my_model import *

# Merge metadata
for table in SQLModel.metadata.tables.values():
    table.tometadata(SQLModel.metadata)

target_metadata = SQLModel.metadata
```

Alternatively, you can uncomment the dynamic import code in `alembic/env.py` to
automatically import all generated models from the `schemas/generated`
directory.

### b. Create a Migration

Generate a new migration file using the `alembic revision` command:

```bash
alembic revision --autogenerate -m "Add my_snake_case_name table"
```

### c. Apply the Migration

Apply the migration to your database using the `alembic upgrade` command:

```bash
alembic upgrade head
```

By following these steps, you can effectively use LinkML to define your data
models and generate SQLAlchemy models for your database, while maintaining a
clean and organized migration history with Alembic.
