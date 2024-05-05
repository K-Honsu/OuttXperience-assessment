from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from decouple import config

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Anjola123@",
    host="localhost",
    database="fastapi-assessment",
    port=5432
)

engine = create_engine(url)
print(engine)
Session = sessionmaker(bind=engine)
session = Session()