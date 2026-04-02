FROM python:3.14.3

# set working directory
WORKDIR /app

ARG HOST_USER
ARG HOST_USER_ID
ARG HOST_GROUP
ARG HOST_GROUP_ID
ARG TIMEZONE=Europe/Madrid

# Create a non-root user and config timezone
RUN groupadd -g ${HOST_GROUP_ID} ${HOST_GROUP} \
    && useradd -r -u ${HOST_USER_ID} -g ${HOST_GROUP} -s /bin/bash -m ${HOST_USER} \
    && chown -R ${HOST_USER}:${HOST_GROUP} /app \
    && apt-get update && apt-get install -y tzdata curl \
    && apt-get install -y iputils-ping \
    && ln -fs /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
    && echo "${TIMEZONE}" > /etc/timezone

# Install Node.js for nodemon in development image
RUN curl -sL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g nodemon

# Install uv
RUN pip install uv

USER ${HOST_USER}

# start app
CMD ["nodemon", "--exec", "uv", "run", "main.py"]
