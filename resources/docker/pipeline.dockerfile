FROM ghcr.io/prefix-dev/pixi:0.56.0 AS build

# copy source code, pixi.toml and pixi.lock to the container
COPY . /app
WORKDIR /app

# Remove any existing pixi environment (if any)
RUN rm -rf /app/.pixi

# run the `install` command (or any other). This will also install the dependencies into `/app/.pixi`
# assumes that you have a `prod` environment defined in your pixi.toml
RUN pixi install -e etl
# Create the shell-hook bash script to activate the environment
RUN pixi shell-hook -e etl > /shell-hook.sh

# extend the shell-hook script to run the command passed to the container
RUN echo 'exec "$@"' >> /shell-hook.sh

FROM ubuntu:24.04 AS production

# only copy the production environment into prod container
# please note that the "prefix" (path) needs to stay the same as in the build container
COPY --from=build /app/.pixi/envs/etl /app/.pixi/envs/etl
COPY --from=build /shell-hook.sh /shell-hook.sh
# copy the source so editable installs resolve correctly
COPY --from=build /app/src /app/src
# copy alembic configuration and migrations
COPY --from=build /app/alembic.ini /app/alembic.ini
COPY --from=build /app/alembic /app/alembic
# copy Prefect flow entrypoint and deployment config
COPY --from=build /app/resources/prefect/run_prefect_flow.py /app/run_prefect_flow.py
COPY --from=build /app/resources/prefect/prefect.yaml /app/prefect.yaml

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

WORKDIR /app
EXPOSE 4200

USER appuser

# set the entrypoint to the shell-hook script (activate the environment and run the command)
# no more pixi needed in the prod container
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
