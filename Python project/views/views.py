from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import json
from Database.db import *
from sqlalchemy.exc import SQLAlchemyError


Base = declarative_base()


app = Flask(__name__)

engine = create_engine('sqlite:///university.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/attestations', methods=['POST'])
def create_attestation_api():
    data = request.get_json()
    student_id = data.get('student_id')
    subject_name = data.get('subject_name')
    first_att = data.get('first_att')
    second_att = data.get('second_att')
    final_att = data.get('final_att')

    create_attestation(student_id, subject_name, first_att, second_att, final_att)

    return jsonify({'message': 'Attestation put successfully'}), 201

@app.route('/attestations/<int:student_id>/<string:subject_name>', methods=['GET'])
def get_attestation_by_ids_api(student_id, subject_name):
    try:
        attestation = get_attestation_by_ids(student_id, subject_name)
        return attestation
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    
@app.route('/attestations', methods=['GET'])
def get_attestation_api():
    try:
        attestation = get_attestations()
        return attestation
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    
@app.route('/users', methods=['POST'])
def create_user_api():
    try:
        data = request.get_json()
        create_user(data['login'], data['password'], data['name'], data['surname'], data['age'])
        return jsonify({'message': 'User created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/users', methods=['GET'])
def get_users_api():
    try:
        users = get_users()
        return users, 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    

@app.route('/users/<int:user_id>',methods = ['GET'])
def get_user_by_id_api(user_id):
    user = get_user_by_id(user_id)
    if user:
        return user, 200
    else:
         return jsonify({'error': f'Student with ID {user_id} not found'}), 404
    
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_api(user_id):
    try:
        data = request.get_json()
        update_user(user_id, data)
        return jsonify({'message': f'User with ID {user_id} updated successfully'}), 200
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_api(user_id):
    try:
        delete_user(user_id)
        return jsonify({'message': f'User with ID {user_id} deleted successfully'}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/journal-entries', methods=['POST'])
def create_journal_entry_api():
    try:
        data = request.get_json()
        create_journal_entry(data['subject_name'], data['student_id'], data['mark'], data['attendance'])
        return jsonify({'message': 'Journal entry created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@app.route('/journal-entries/<int:student_id>/<string:subject_name>', methods=['GET'])
def get_journal_entry_by_id_api(student_id,subject_name):
    try:
        entry = get_journal_entry_by_student_id(student_id,subject_name)
        return entry
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    
@app.route('/lesson-participations', methods=['POST'])
def create_lesson_participation_api():
    try:
        data = request.get_json()
        create_lesson_participation(data['student_id'], data['subject_name'])
        return jsonify({'message': 'Lesson participation created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/lesson-participations', methods=['GET'])
def get_lesson_participations_api():
    try:
        participations = get_lesson_participations()
        return participations,200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@app.route('/lesson-participations/<int:student_id>/<string:subject_name>', methods=['GET'])
def get_lesson_participation_by_ids_api(student_id, subject_name):
    try:
        participation = get_lesson_participation_by_ids(student_id, subject_name)
        return participation
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500




@app.route('/subjects', methods=['POST'])
def create_subject_api():
    try:
        data = request.get_json()
        create_subject(data['name'])
        return jsonify({'message': 'Subject created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/subjects', methods=['GET'])
def get_subjects_api():
    try:
        subjects = get_subjects()
        return subjects
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

def delete_subject_api(subject_name):
    try:
        delete_subject(subject_name)
        return jsonify({'message': f'Subject deleted successfully'}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500