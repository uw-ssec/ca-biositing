FROM ghcr.io/prefix-dev/pixi:0.56.0 AS build

# copy source code, pixi.toml and pixi.lock to the container
COPY . /app
WORKDIR /app

# Remove any existing pixi environment (if any)
RUN rm -rf /app/.pixi

# Install the webservice pixi environment
RUN pixi install -e webservice
# Create the shell-hook bash script to activate the environment
RUN pixi shell-hook -e webservice > /shell-hook.sh

# extend the shell-hook script to run the command passed to the container
RUN echo 'exec "$@"' >> /shell-hook.sh

FROM ubuntu:24.04 AS production

# only copy the production environment into prod container
# please note that the "prefix" (path) needs to stay the same as in the build container
COPY --from=build /app/.pixi/envs/webservice /app/.pixi/envs/webservice
COPY --from=build /shell-hook.sh /shell-hook.sh
# copy the source so editable installs resolve correctly
COPY --from=build /app/src /app/src

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
EXPOSE 8080

# set the entrypoint to the shell-hook script (activate the environment and run the command)
# no more pixi needed in the prod container
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
CMD ["uvicorn", "ca_biositing.webservice.main:app", "--host", "0.0.0.0", "--port", "8080"]
