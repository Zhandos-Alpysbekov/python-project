from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import DateTime as SA_DateTime
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)

    student = relationship('Student', back_populates='user', uselist=False)
    teacher = relationship('Teacher', back_populates='user', uselist=False)

class Student(Base):
    __tablename__ = 'students'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    faculty = Column(String)
    user = relationship('User', back_populates='student')

    journal_entries = relationship('JournalEntry', back_populates='student')
    attestations = relationship('Attestation', back_populates='student')
    lesson_participation = relationship('LessonParticipation', back_populates='student')

class Teacher(Base):
    __tablename__ = 'teachers'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', back_populates='teacher')
    subjects = relationship('Subject', back_populates='teacher')

    

class Subject(Base):
    __tablename__ = 'subjects'

    name = Column(String, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.user_id'))
    teacher = relationship('Teacher', back_populates='subjects')

    journal_entries = relationship('JournalEntry', back_populates='subject')
    attestations = relationship('Attestation', back_populates='subject')
    lesson_participation = relationship('LessonParticipation', back_populates='subject')

class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True)
    subject_name = Column(String, ForeignKey('subjects.name'))
    student_id = Column(Integer, ForeignKey('students.user_id'))
    mark = Column(Integer)
    attendance = Column(Integer)
    entry_date = Column(SA_DateTime, default=datetime.utcnow)

    subject = relationship('Subject', back_populates='journal_entries')
    student = relationship('Student', back_populates='journal_entries')

class Attestation(Base):
    __tablename__ = 'attestations'

    student_id = Column(Integer, ForeignKey('students.user_id'), primary_key=True)
    subject_name = Column(String, ForeignKey('subjects.name'), primary_key=True)
    first_att = Column(Integer)
    second_att = Column(Integer)
    final_att = Column(Integer)
    total_att = Column(Integer)

    student = relationship('Student', back_populates='attestations')
    subject = relationship('Subject', back_populates='attestations')

class LessonParticipation(Base):
    __tablename__ = 'lesson_participation'

    student_id = Column(Integer, ForeignKey('students.user_id'), primary_key=True)
    subject_name = Column(String, ForeignKey('subjects.name'), primary_key=True)

    student = relationship('Student', back_populates='lesson_participation')
    subject = relationship('Subject', back_populates='lesson_participation')

# Создание таблиц в базе данных
engine = create_engine('sqlite:///university.db')
Base.metadata.create_all(engine)
