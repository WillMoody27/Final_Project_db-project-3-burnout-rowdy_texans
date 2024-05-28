"""
CS3810: Principles of Database Systems
Instructor: Thyago Mota
Student(s): William Hellems-Moody, David Carter
Description: SQLAlchemy Models
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

Base = declarative_base()

class BurnoutQuestion(Base):
    __tablename__ = 'burnout_questions'
    number = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)

class Surveyee(Base): 
    __tablename__ = 'surveyees'
    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)

class Result(Base): 
    __tablename__ = 'results'
    question_number = Column(Integer, ForeignKey("burnout_questions.number"), primary_key=True)
    burnout_question = relationship("BurnoutQuestion")
    surveyee_email = Column(String, ForeignKey("surveyees.email"), primary_key=True)
    surveyee = relationship("Surveyee")
    date = Column(Date, primary_key=True)
    rate = Column(Integer, nullable=False)