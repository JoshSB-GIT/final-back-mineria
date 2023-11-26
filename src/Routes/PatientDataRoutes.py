import csv
from flask import make_response, jsonify, Blueprint, request
from flask_cors import cross_origin
from Models.PatientDataModel import PatientDataModel
from flask_jwt_extended import (
    JWTManager, jwt_required,
    create_access_token
)
from Config.Config import Configuration
from DB.DB import DataBase


patient = Blueprint('patient', __name__)
app = DataBase().app
jwt = JWTManager(app)

app = DataBase().app
patient_data_model = PatientDataModel()


@patient.route('/get_patient_data', methods=['GET'])
@cross_origin()
@jwt_required()
def get_patient_data():
    code = 200
    message = 'Data loaded successfully'

    try:
        data = patient_data_model.get_all_patient_data()
    except Exception as e:
        code = 400
        message = "Error: " + str(e)

    return make_response(
        jsonify(
            {"message": message, "data": data, "code": code}
        ), code)


@patient.route('/add_patient_data', methods=['POST'])
@cross_origin()
@jwt_required()
def add_patient_data():
    code = 200
    message = 'Data added successfully'

    try:
        # Obtén los datos del cuerpo de la solicitud
        data = request.json

        # Llama al método add_patient_data del modelo con los datos de la solicitud
        patient_data_model.add_patient_data(
            patient_id=data.get('patient_id', None),
            age=data.get('age', None),
            cholesterol=data.get('cholesterol', None),
            blood_pressure=data.get('blood_pressure', None),
            heart_rate=data.get('heart_rate', None),
            diabetes=data.get('diabetes', None),
            family_history=data.get('family_history', None),
            smoking=data.get('smoking', None),
            obesity=data.get('obesity', None),
            alcohol_consumption=data.get('alcohol_consumption', None),
            exercise_hours_per_week=data.get('exercise_hours_per_week', None),
            diet=data.get('diet', None),
            previous_heart_problems=data.get('previous_heart_problems', None),
            medication_use=data.get('medication_use', None),
            stress_level=data.get('stress_level', None),
            sedentary_hours_per_day=data.get('sedentary_hours_per_day', None),
            income=data.get('income', None),
            bmi=data.get('bmi', None),
            triglycerides=data.get('triglycerides', None),
            physical_activity_days_per_week=data.get(
                'physical_activity_days_per_week', None),
            sleep_hours_per_day=data.get('sleep_hours_per_day', None),
            country=data.get('country', None),
            continent=data.get('continent', None),
            hemisphere=data.get('hemisphere', None),
            heart_attack_risk=data.get('heart_attack_risk', None),
            user_id=data.get('user_id', None),
            sex=data.get('sex', None)
        )
    except Exception as e:
        code = 400
        message = "Error: " + str(e)

    print(message, code)
    return make_response(
        jsonify(
            {"message": message, "code": code}
        ), code)


@patient.route('/delete_patient_data/<int:patient_data_id>', methods=['DELETE'])
@cross_origin()
@jwt_required()
def delete_patient_data(patient_data_id):
    code = 200
    message = 'Data deleted successfully'

    try:
        patient_data_model.delete_patient_data(patient_data_id)
    except Exception as e:
        code = 400
        message = "Error: " + str(e)

    return make_response(
        jsonify(
            {"message": message, "code": code}
        ), code)


@patient.route('/file/add_patient_data', methods=['POST'])
@cross_origin()
@jwt_required()
def add_patient_data_file():
    code = 200
    message = 'Data added successfully'

    try:
        # Obtén el archivo CSV del cuerpo de la solicitud
        csv_file = request.files['file']
        if not csv_file:
            message = ("No se proporcionó un archivo CSV")
            code = 400

        # Lee el contenido del CSV
        csv_content = csv_file.read().decode('utf-8')

        # Utiliza la biblioteca csv para procesar el contenido
        csv_reader = csv.DictReader(csv_content.splitlines())
        for row in csv_reader:

            # Asigna el valor predeterminado None a user_id si no está presente en el diccionario
            user_id = row.pop('user_id', 1)

            # Llama al método add_patient_data del modelo con los datos del CSV
            patient_data_model.add_patient_data(user_id=user_id, **row)

    except Exception as e:
        code = 400
        message = "Error: " + str(e)

    return make_response(
        jsonify(
            {"message": message, "code": code}
        ), code)
