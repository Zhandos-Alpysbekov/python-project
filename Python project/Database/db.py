from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.modelsDB import User, Student, Teacher, Subject, JournalEntry, Attestation, LessonParticipation
from datetime import datetime
import json


engine = create_engine('sqlite:///university.db')
Session = sessionmaker(bind=engine)
session = Session()

#FOR USER
def create_user(login, password, name, surname, age):
    new_user = User(login=login, password=password, name=name, surname=surname, age=age)
    session.add(new_user)
    session.commit()

def get_users():
    users = session.query(User).all()
    user_list = []
    for user in users:
        user_dict = {
            'id': user.id,
            'login': user.login,
            'password': user.password,
            'name': user.name,
            'surname': user.surname,
            'age': user.age
        }
        user_list.append(user_dict)
    return json.dumps(user_list)

def get_user_by_id(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user_dict = {
            'id': user.id,
            'login': user.login,
            'password': user.password,
            'name': user.name,
            'surname': user.surname,
            'age': user.age
        }
        return json.dumps(user_dict)
    else:
        return json.dumps({'error': 'User not found'})

def update_user(user_id, new_data):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        for key, value in new_data.items():
            setattr(user, key, value)
        session.commit()

def delete_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()

#FOR SUBJECT
def create_subject(name, teacher=None):
    new_subject = Subject(name=name)
    if teacher:
        new_subject.assign_teacher(teacher)
    session.add(new_subject)
    session.commit()

def get_subjects():
    subjects = session.query(Subject).all()
    subject_list = [{'name': subject.name} for subject in subjects]
    return json.dumps(subject_list)

def get_subject_by_name(subject_name):
    subject = session.query(Subject).filter_by(name=subject_name).first()
    if subject:
        subject_dict = {'name': subject.name}
        return json.dumps(subject_dict)
    else:
        return json.dumps({'error': 'Subject not found'})

def update_subject(subject_name, new_data):
    subject = session.query(Subject).filter_by(name=subject_name).first()
    if subject:
        for key, value in new_data.items():
            setattr(subject, key, value)
        session.commit()

def delete_subject(subject_name):
    subject = session.query(Subject).filter_by(name=subject_name).first()
    if subject:
        session.delete(subject)
        session.commit()

#FOR STUDENT
def create_student(login, password, name, surname, age, faculty):

    new_user = User(login=login, password=password, name=name, surname=surname, age=age)
    new_student = Student(faculty=faculty, user=new_user)

    session.add(new_user)
    session.commit()

def get_students():
    students = session.query(Student).all()
    student_list = [{'user_id': student.user_id, 'faculty': student.faculty} for student in students]
    return json.dumps(student_list)

def get_student_by_id(student_id):
    student = session.query(Student).filter_by(user_id=student_id).first()
    if student:
        student_dict = {'user_id': student.user_id, 'faculty': student.faculty}
        return json.dumps(student_dict)
    else:
        return json.dumps({'error': 'Student not found'})

def update_student(student_id, new_data):
    student = session.query(Student).filter_by(user_id=student_id).first()
    if student:
        for key, value in new_data.items():
            setattr(student, key, value)
        session.commit()

def delete_student(student_id):
    student = session.query(Student).filter_by(user_id=student_id).first()
    if student:
        session.delete(student)
        session.commit()


#FOR TEACHER
def create_teacher(login, password, name, surname, age):
    new_user = User(login=login, password=password, name=name, surname=surname, age=age)
    new_teacher = Teacher(user=new_user)

    session.add(new_user)
    session.commit()

def get_teachers():
    teachers = session.query(Teacher).all()
    teacher_list = [{'user_id': teacher.user_id} for teacher in teachers]
    return json.dumps(teacher_list)

def get_teacher_by_id(teacher_id):
    teacher = session.query(Teacher).filter_by(user_id=teacher_id).first()
    if teacher:
        teacher_dict = {'user_id': teacher.user_id}
        return json.dumps(teacher_dict)
    else:
        return json.dumps({'error': 'Teacher not found'})
    
def update_teacher(teacher_id, new_data):
    teacher = session.query(Teacher).filter_by(user_id=teacher_id).first()
    if teacher:
        for key, value in new_data.items():
            setattr(teacher, key, value)
        session.commit()

def delete_teacher(teacher_id):
    teacher = session.query(Teacher).filter_by(user_id=teacher_id).first()
    if teacher:
        session.delete(teacher)
        session.commit()

#FOR JOURNAL
def create_journal_entry(subject_name, student_id, mark, attendance):
    lesson_participation = session.query(LessonParticipation).filter_by(student_id=student_id, subject_name=subject_name).first()
    if lesson_participation:
        new_entry = JournalEntry(subject_name=subject_name, student_id=student_id, mark=mark, attendance=attendance,entry_date = datetime.now)
        session.add(new_entry)
        session.commit()
    else:
        return json.dumps({'error': f"Error: Student ID {student_id} has no lessons for subject {subject_name}. Mark not added."})


def get_journal_entries():
    entries = session.query(JournalEntry).all()
    entry_list = [{'id': entry.id, 'subject_name': entry.subject_name, 'student_id': entry.student_id, 'mark': entry.mark, 'attendance': entry.attendance} for entry in entries]
    return json.dumps(entry_list)

def get_journal_entry_by_student_id(student_id, subject_name):
    entry = session.query(JournalEntry).filter_by(student_id=student_id,subject_name = subject_name).first()
    if entry:
        entry_dict = {'id': entry.id, 'subject_name': entry.subject_name, 'student_id': entry.student_id, 'mark': entry.mark, 'attendance': entry.attendance}
        return json.dumps(entry_dict)
    else:
        return json.dumps({'error': 'Journal entry not found'})
    
def update_journal_entry(entry_id, new_data):
    entry = session.query(JournalEntry).filter_by(id=entry_id).first()
    if entry:
        for key, value in new_data.items():
            setattr(entry, key, value)
        session.commit()

def delete_journal_entry(entry_id):

    entry = session.query(JournalEntry).filter_by(id=entry_id).first()
    if entry:
        session.delete(entry)
        session.commit()

#FOR ATTESTATION
def create_attestation(student_id, subject_name, first_att, second_att, final_att):
    lesson_participation = session.query(LessonParticipation).filter_by(student_id=student_id, subject_name=subject_name).first()

    if lesson_participation:
        # The student has lessons for the subject, proceed with attestation
        new_attestation = Attestation(student_id=student_id, subject_name=subject_name,
                                      first_att=first_att, second_att=second_att, final_att=final_att)
        session.add(new_attestation)
        session.commit()
        print(f"Attestation added for Student ID {student_id}, Subject: {subject_name}: First Att={first_att}, Second Att={second_att}, Final Att={final_att}")
    else:
        return json.dumps({'error': f"Error: Student ID {student_id} has no lessons for subject {subject_name}. Mark not added."})

    
def get_attestations():
    attestations = session.query(Attestation).all()
    attestation_list = [{'student_id': attestation.student_id, 'subject_name': attestation.subject_name, 'first_att': attestation.first_att, 'second_att': attestation.second_att, 'final_att': attestation.final_att, 'total_att': attestation.total_att} for attestation in attestations]
    return json.dumps(attestation_list)

def get_attestation_by_ids(student_id, subject_name):
    attestation = session.query(Attestation).filter_by(student_id=student_id, subject_name=subject_name).first()
    if attestation:
        attestation_dict = {'student_id': attestation.student_id, 'subject_name': attestation.subject_name, 'first_att': attestation.first_att, 'second_att': attestation.second_att, 'final_att': attestation.final_att, 'total_att': attestation.total_att}
        return json.dumps(attestation_dict)
    else:
        return json.dumps({'error': 'Attestation not found'})
def update_attestation(student_id, subject_name, new_data):
    attestation = session.query(Attestation).filter_by(student_id=student_id, subject_name=subject_name).first()
    if attestation:
        for key, value in new_data.items():
            setattr(attestation, key, value)
        session.commit()

def delete_attestation(student_id, subject_name):
    attestation = session.query(Attestation).filter_by(student_id=student_id, subject_name=subject_name).first()
    if attestation:
        session.delete(attestation)
        session.commit()

#FOR LESSON
def create_lesson_participation(student_id, subject_name):
    new_participation = LessonParticipation(student_id=student_id, subject_name=subject_name)
    session.add(new_participation)
    session.commit()

def get_lesson_participations():
    participations = session.query(LessonParticipation).all()
    participation_list = [{'student_id': participation.student_id, 'subject_name': participation.subject_name} for participation in participations]
    return json.dumps(participation_list)

def get_lesson_participation_by_ids(student_id, subject_name):
    participation = session.query(LessonParticipation).filter_by(student_id=student_id, subject_name=subject_name).first()
    if participation:
        participation_dict = {'student_id': participation.student_id, 'subject_name': participation.subject_name}
        return json.dumps(participation_dict)
    else:
        return json.dumps({'error': 'Lesson participation not found'})
    
def update_lesson_participation(student_id, subject_name, new_data):
    participation = session.query(LessonParticipation).filter_by(student_id=student_id, subject_name=subject_name).first()
    if participation:
        for key, value in new_data.items():
            setattr(participation, key, value)
        session.commit()

def delete_lesson_participation(student_id, subject_name):
    participation = session.query(LessonParticipation).filter_by(student_id=student_id, subject_name=subject_name).first()
    if participation:
        session.delete(participation)
        session.commit()