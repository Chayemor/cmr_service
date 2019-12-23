# Official Python runtime as a parent image
FROM python:3.8

# Set default value through ARG, then get the value from from command-line argument
ARG APP_ENV=prod
ENV APP_ENV ${APP_ENV}

# Ensure Python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# create root
RUN mkdir /django-docker

# Set the working directory
WORKDIR /django-docker

# Load only requirements and install
ADD ./requirements /django-docker/requirements
RUN pip install -r /django-docker/requirements/${APP_ENV}.txt

# Load the current directory contents into the container at WORKDIR
ADD . /django-docker

ADD ./entrypoint-${APP_ENV}.sh /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]
