FROM python:3.14.3

# set working directory
WORKDIR /app

ARG HOST_USER
ARG HOST_USER_ID
ARG HOST_GROUP
ARG HOST_GROUP_ID
ARG TIMEZONE=Europe/Madrid

COPY ./develop/docker-entrypoint.sh /usr/local/bin/docker-app-entrypoint
RUN chmod +x /usr/local/bin/docker-app-entrypoint
ENTRYPOINT ["docker-app-entrypoint"]

# Create a non-root user and config timezone
RUN groupadd -g ${HOST_GROUP_ID} ${HOST_GROUP} \
    && useradd -r -u ${HOST_USER_ID} -g ${HOST_GROUP} -s /bin/bash -m ${HOST_USER} \
    && chown -R ${HOST_USER}:${HOST_GROUP} /app \
    && apt-get update && apt-get install -y tzdata curl \
    && apt-get install -y iputils-ping \
    && ln -fs /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
    && echo "${TIMEZONE}" > /etc/timezone

# Install uv
RUN pip install uv

USER ${HOST_USER}

# start app
CMD ["fastapi", "dev"]
