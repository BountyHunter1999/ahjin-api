# Before we try to run the program

# For Local Testing

1. Create a .env file in the same path as the Dockerfile
2. The Content of the .env files are as:
    - `DJANGO_SECRET_KEY` your django application secret key
    - `DJANGO_DEBUG` as we are testing it should be like `DJANGO_DEBUG=True`
    - `DJANGO_ALLOWED_HOSTS` add the addresses u will allow `DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 0.0.0.0  <anything_here>` [::1]`
    - `POSTGRES_HOST` make this the database container service name
    - `POSTGRES_NAME` your choice
    - `POSTGRES_USER` your choice
    - `POSTGRES_PASSWORD` your choice
    - `GMAIL_ACC` and `GMAIL_PW` set them to the account you want to send mail from
    - `EMAIL_PORT` also define the email port
    - `EMAIL_USE_TLS` you can set this to any boolean value
    - `EMAIL_HOST=smtp.gmail.com` you can select anything you want
    - `EMAIL_VERIFICATION_OPTION=mandatory` choose your option from django provided options
    - `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` for smtp this requires `GMAIL_ACC`, `GMAIL_PW`
    - `KHALTI_SECRET_KEY` use the SECRET_KEY Provided by Khalti
    - `FRONT_END_URL` front-end url u want to map to
3. `docker-compose up --build` to run the backend service

# For production testing

1. Create a `.env-prod` file in the same path as the Dockerfile
2. include fields the same as above with `POSTGRES_HOST` name to container service name `db_prod` and all others
3. `docker-compose -f docker-compose-prod.yaml up --build` to run the backend and frontend with nginx gunicorn and all others
