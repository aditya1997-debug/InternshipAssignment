from sqlalchemy import Column, Integer, String
from database import Base

# Define To Do class inheriting from Base
class ModelToDo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(String(256))