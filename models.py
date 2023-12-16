
from sqlalchemy import Column, Integer, String, ForeignKey, Date, create_engine, text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("1"))
    fullname = Column(String(120), nullable=False)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("1"))
    name = Column(String(20), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("1"))
    fullname = Column(String(120), nullable=False)
    group_id = Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship('Group', backref='students')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("1"))
    name = Column(String(120), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship('Teacher', backref='disciplines')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("1"))
    grade = Column(Integer, nullable=False)
    date_of = Column('date_of', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    subjects_id = Column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'))
    student = relationship('Student', backref='grade')
    subject = relationship('Subject', backref='grade')



engine = create_engine('postgresql://postgres:pass@localhost/myhw7', echo=True)

#Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)