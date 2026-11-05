from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
dburl="postgresql://postgres:sindhu@localhost:5432/Fastapiproject2"
engine=create_engine(dburl)
sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)