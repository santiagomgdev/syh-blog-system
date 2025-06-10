from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)
    
    def soft_delete(self):
        self.deleted_at = datetime.now()

class CustomBase(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)