# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Pixi
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://pixi.sh/install.sh | bash && \
    mv /root/.pixi/bin/pixi /usr/local/bin/pixi

# Copy the pixi configuration files
COPY pixi.toml pixi.lock* ./

# Install project dependencies using Pixi
RUN pixi install

# Set the Python path
ENV PYTHONPATH /app

# Copy the rest of the application's code into the container at /app
COPY src ./src
COPY src/pipeline/alembic.ini .

# Command to run the application
CMD ["bash"]
