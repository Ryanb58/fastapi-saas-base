from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite://"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.bind = engine
