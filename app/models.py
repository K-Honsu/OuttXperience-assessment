from database import engine
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    author = Column(String)
    year = Column(Integer)
    isbn = Column(String)
    created_at = Column(TIMESTAMP(timezone=True))
    
    def save(self, **kwargs):
        for key, value in kwargs:
            if key != "id" and key != "_sa_instance_state":
                self.__setattr__()


Base.metadata.create_all(bind=engine)
