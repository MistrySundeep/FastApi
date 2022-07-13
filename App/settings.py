import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('config.env'))

# DATABASE ENV VARIABLES

DB_HOST = os.environ.get('DB_HOST')
PG_USER = os.environ.get('PG_USER')
PG_PW = os.environ.get('PG_PW')
PG_DB = os.environ.get('PG_DB')
DB_URL = os.environ.get('DB_URL')
