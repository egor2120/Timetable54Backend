import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, Sequence, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.functions import now

from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL="postgresql://postgres:6282@127.0.0.1:5433/postgres"

engine = sqlalchemy.create_engine(DATABASE_URL())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    login = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    real_name = Column(String(50), nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    register_date = Column(DateTime, nullable=False, default=now())
    status = Column(String(1), default='1', nullable=False)
    role = Column(String(10), default='user', nullable=False)

    photos = relationship("Photo", back_populates="owner")
    products = relationship("Cart", back_populates="user")