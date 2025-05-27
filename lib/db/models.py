# SQLAlchemy models for File, Folder, and UserAction
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class Folder(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    files = relationship('File', back_populates='folder')

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    original_path = Column(String, nullable=False)
    new_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    date_moved = Column(DateTime, default=datetime.datetime.utcnow)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    folder = relationship('Folder', back_populates='files')

class UserAction(Base):
    __tablename__ = 'user_actions'
    id = Column(Integer, primary_key=True)
    action_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String)
