# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install  gunicorn --no-cache-dir && pip install --no-cache-dir -r requirements.txt


# Обновление пакетов и установка Redis
RUN apt-get update && apt-get install -y redis-server


COPY . /app/
# USER root
RUN         set -x \
            && apt-get -qq update \
            && apt-get install -yq --no-install-recommends pgbouncer \
            && apt-get purge -y --auto-remove \
            && rm -rf /var/lib/apt/lists/*



COPY pgbouncer.ini /etc/pgbouncer/pgbouncer.ini

RUN touch /app/pgbouncer.pid && chmod 644 /app/pgbouncer.pid && chown 1000:1000 /app/pgbouncer.pid



# Run the entrypoint script when the container starts
CMD ["bash", "entrypoint.sh"]

# sudo apt install nginx