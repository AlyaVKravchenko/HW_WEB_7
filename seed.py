from datetime import datetime

from faker import Faker
import random

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from models import create_engine, Base, Student, Group, Teacher, Subject, Grade

fake = Faker('uk-UA')
engine = create_engine('postgresql://postgres:pass@localhost/myhw7', echo=True)

Session = sessionmaker(bind=engine)
session = Session()


def generate_fake_group_name():
    department = fake.random_element(elements=('ПБ', 'ПК', 'ПГ'))
    group_number = fake.random_int(min=10, max=99)

    return f"{department}-{group_number}"


def generate_fake_date(start_date='2023-09-01', end_date=datetime.now().strftime('%Y-%m-%d')):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    fake_datetime = fake.date_time_between(start_date=start_datetime, end_date=end_datetime)
    return fake_datetime


def insert_teachers():
    teachers = []
    for _ in range(5):
        teacher = Teacher(
            fullname=fake.name(),
        )
        teachers.append(teacher)
        session.add(teacher)
    return teachers


def insert_groups():
    groups = []
    for _ in range(3):
        group = Group(
            name=generate_fake_group_name(),
        )
        groups.append(group)
        session.add(group)
    return groups


def insert_student():
    groups = session.query(Group).all()
    for _ in range(50):
        student = Student(
            fullname=fake.name(),
            group=random.choice(groups)
        )
        session.add(student)


def insert_subject():
    teachers = session.query(Teacher).all()
    subjects_list=['Вища математика', 'Фізика', 'Хімія',
                  'Програмування', 'Українська мова', 'Література',
                  'Автоматизація', 'Електротехніка']
    existing_subjects = session.query(Subject.name).distinct().all()
    existing_subjects = [subject[0] for subject in existing_subjects]

    for _ in range(8):
        # Генеруємо унікальне ім'я предмета
        new_subject_name = random.choice([subject for subject in subjects_list if subject not in existing_subjects])

        subject = Subject(
            name=new_subject_name,
            teacher=random.choice(teachers)
        )
        session.add(subject)
        existing_subjects.append(new_subject_name)


def insert_grade():
    subjects = session.query(Subject).all()
    students = session.query(Student).all()

    for student in students:
        num_grades = random.randint(12, 20)
        selected_subjects = random.sample(subjects, min(num_grades, len(subjects)))

        for subject in selected_subjects:
            num_grades_per_subject = random.randint(1, 5)
            grades = [random.randint(0, 100) for _ in range(num_grades_per_subject)]
            grade_dates = [generate_fake_date() for _ in range(num_grades_per_subject)]

            for grade, grade_date in zip(grades, grade_dates):
                grade_entry = Grade(
                    grade=grade,
                    date_of=grade_date,
                    student=student,
                    subject=subject
                )
                session.add(grade_entry)


if __name__ == '__main__':
    try:
        insert_teachers()
        insert_groups()
        insert_student()
        insert_subject()
        insert_grade()
        session.commit()

    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()