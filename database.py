from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url='postgresql://postgres:123456789@localhost:5432/praveen'
engine=create_engine(db_url)
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)

