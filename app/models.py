from ast import In
from enum import unique
import string
from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db import Base,engine
import datetime

# Classes

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), unique=True)
    scope = relationship("Scope", cascade="all, delete", passive_deletes=True)

class Scope(Base):
    __tablename__ = 'scopes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(200), unique=True)
    id_project = Column(Integer, ForeignKey('projects.id'), nullable=True)
    url = relationship("Url", cascade="all, delete")

class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String(200))
    id_scope = Column(Integer, ForeignKey('scope.id'), nullable=True)
    form = relationship("Form", cascade="all, delete")

class Form(Base):
    __tablename__ = 'forms'
    id = Column(Integer, autoincrement=True, primary_key=True)
    action = Column(String(200))
    method = Column(String(20))
    id_url = Column(Integer, ForeignKey('urls.id'), nullable=True)
    input = relationship("Input", cascade="all, delete")

class Input(Base):
    __tablename__ = 'inputs'
    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(String(50))
    name = Column(String(200))
    value = Column(String(500))
    id_form = Column(Integer, ForeignKey('forms.id'), nullable=True)

Base.metadata.create_all(engine)