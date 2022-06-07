import os

my_env = os.environ

host = my_env['DB_HOST']
db = my_env['DB_NAME']
user = my_env['DB_USER']
pw = my_env['DB_PASS']
# host = os.environ.get('DB_HOST')
# db = os.environ.get('DB_NAME')
# user = os.environ.get('DB_USER')
# pw = os.environ.get('DB_PASS')

DATABASE_CONNECTION_URI =  f'postgresql+psycopg2://{user}:{pw}@{host}:5434/{db}'