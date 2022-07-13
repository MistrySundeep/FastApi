import psycopg2
from App.settings import DB_URL, DB_HOST, PG_DB, PG_PW, PG_USER
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creates an SQLAlchemy engine
engine = create_engine(DB_URL)

# Each instance of this class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Used to create database models
Base = declarative_base()

# From psycopg2 used to set up the connection to the postgres database
conn_str = f"host='{DB_HOST}' dbname='{PG_DB}' user='{PG_USER}' password='{PG_PW}'"
conn = psycopg2.connect(conn_str)
