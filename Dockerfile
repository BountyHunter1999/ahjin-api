# Pull base image
FROM python:3.9.13-alpine3.16

# Environment Variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# installing required packages
COPY ./requirements.txt /requirements.txt

# installing postgressql-client
RUN apk add --update --no-cache postgresql-client

# adding temporary packages for requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
     gcc libc-dev linux-headers  rust cargo \
     postgresql-dev libffi-dev

RUN pip install -r /requirements.txt
RUN pip install python-dotenv

# removing the temporary packages
RUN apk del .tmp-build-deps


# Set work directory
RUN mkdir /app
WORKDIR /app

# Copy project
COPY ./app /app

# Copy the env variables
# COPY .env .env docker-compose provides this

# Create a user and switch to it
RUN adduser -D user
USER user

EXPOSE 8000

# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "app.wsgi:application"]