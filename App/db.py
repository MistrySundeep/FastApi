import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The URL for the database in use
DB_URL = 'postgresql://postgres:ipr1smData@localhost:5432/AddressData'

# Creates an SQLalchemy engine
engine = create_engine(DB_URL)

# Each instance of this class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Used to create database models
Base = declarative_base()

# From psycopg2 used to set up the conncetion to the postgres database
conn_str = "host='localhost' dbname='AddressData' user='postgres' password='ipr1smData'"
conn = psycopg2.connect(conn_str)
