📄 Description

This PR implements a master "source-of-truth" LinkML schema within the
datamodels package. This LinkML schema is then used to generate SQLAlchemy
models, which are tracked by alembic and migrated to the postgres database. A
mixi-command was created to generate and clean the sqlalchemy models, as well as
create a migration file with alembic. The readme doc in the datamodels package
has been updated with instructions on how to perform these commands.

There is a persistent issue where inherited attributes in sqlalchemy classes are
being placed at the end of the list of columns (so for example id, created_at,
updated_at are at the end). I am still trying to work out a fix for this...

In addition, there were some small fixes to debug issues with windows pipeline
users. win-64 was added as a platform to the pixi.toml, and asyncpg was added as
a dependency.

There is still a good bit of cleanup and documentation updating that should
occur, but that will be in another PR.
