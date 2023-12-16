from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Teacher, Group

engine = create_engine('postgresql://postgres:pass@localhost/myhw7', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    query = (
        session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc('avg_grade'))
        .limit(5)
    )
    print(query)
    return query.all()


def select_2(subject_name):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    query = (
        session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))
        .join(Grade, Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc('avg_grade'))
        .limit(1)
    )
    return query.first()


def select_3(subject_name):
    """Знайти середній бал у групах з певного предмета."""
    query = (
        session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))
        .join(Student, Grade, Subject)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
    )
    return query.all()


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    query = (
        session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))
    )
    return query.scalar()


def select_5(teacher_name):
    """Знайти які курси читає певний викладач."""
    query = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.fullname == teacher_name)
        .distinct()
    )
    return query.all()


def select_6(group_name):
    """Знайти список студентів у певній групі."""
    query = (
        session.query(Student.fullname)
        .join(Group)
        .filter(Group.name == group_name)
    )
    return query.all()


def select_7(group_name, subject_name):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    query = (
        session.query(Student.fullname, Grade.grade)
        .join(Group, Grade, Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
    )
    return query.all()


def select_8(teacher_name):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    query = (
        session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))
        .join(Subject, Teacher)
        .filter(Teacher.fullname == teacher_name)
    )
    return query.scalar()


def select_9(student_name):
    """Знайти список курсів, які відвідує певний студент."""
    query = (
        session.query(Subject.name)
        .join(Grade, Student)
        .filter(Student.fullname == student_name)
        .distinct()
    )
    return query.all()


def select_10(student_name, teacher_name):
    """ Список курсів, які певному студенту читає певний викладач."""
    query = (
        session.query(Subject.name)
        .join(Grade, Student, Teacher)
        .filter(Student.fullname == student_name, Teacher.fullname == teacher_name)
        .distinct()
    )
    return query.all()