# Pull base image
FROM python:3.11-rc-alpine

# Environment Variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# installing required packages
COPY ./requirements.txt /requirements.txt

# installing postgressql-client
RUN apk add --update --no-cache postgresql-client

# adding temporary packages for requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
     gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# removing the temporary packages
RUN apk del .tmp-build-deps


# Set work directory
RUN mkdir /app
WORKDIR /app

# Copy project
COPY ./app /app

# Create a user and switch to it
RUN adduser -D user
USER user