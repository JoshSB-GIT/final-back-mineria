from DB.DB import DataBase
from Tools.QueryTools import QueryTools
from datetime import datetime


class PatientDataModel(DataBase):

    QUERYS = QueryTools()

    def __init__(self, patient_id="", age=0, cholesterol=0, blood_pressure="", heart_rate=0, diabetes=0,
                 family_history=0, smoking=0, obesity=0, alcohol_consumption=0, exercise_hours_per_week=0.0,
                 diet="", previous_heart_problems=0, medication_use=0, stress_level=0, sedentary_hours_per_day=0.0,
                 income=0, bmi=0.0, triglycerides=0, physical_activity_days_per_week=0, sleep_hours_per_day=0.0,
                 country="", continent="", hemisphere="", heart_attack_risk=0, status=1, user_id=0, sex=''):
        super().__init__()
        self.patient_id = patient_id
        self.age = age
        self.cholesterol = cholesterol
        self.blood_pressure = blood_pressure
        self.heart_rate = heart_rate
        self.diabetes = diabetes
        self.family_history = family_history
        self.smoking = smoking
        self.obesity = obesity
        self.alcohol_consumption = alcohol_consumption
        self.exercise_hours_per_week = exercise_hours_per_week
        self.diet = diet
        self.previous_heart_problems = previous_heart_problems
        self.medication_use = medication_use
        self.stress_level = stress_level
        self.sedentary_hours_per_day = sedentary_hours_per_day
        self.income = income
        self.bmi = bmi
        self.triglycerides = triglycerides
        self.physical_activity_days_per_week = physical_activity_days_per_week
        self.sleep_hours_per_day = sleep_hours_per_day
        self.country = country
        self.continent = continent
        self.hemisphere = hemisphere
        self.heart_attack_risk = heart_attack_risk
        self.status = status
        self.user_id = user_id
        self.sex = sex

    def __str__(self):
        return f""""PatientData(patient_id={self.patient_id}, 
        age={self.age}, 
        heart_attack_risk={self.heart_attack_risk})"""

    def get_all_patient_data(self) -> list[dict]:
        cur = self.conn.connection.cursor()
        cur.execute(self.QUERYS.SELECT_ALL_FROM.format('patient_data'))
        data = cur.fetchall()
        cur.close()

        list_patient_data = []

        if data:
            for patient_data in data:
                _patient_data = {
                    'patient_data_id': patient_data[0],
                    'patient_id': patient_data[1],
                    'age': patient_data[2],
                    'cholesterol': patient_data[3],
                    'blood_pressure': patient_data[4],
                    'heart_rate': patient_data[5],
                    'diabetes': patient_data[6],
                    'family_history': patient_data[7],
                    'smoking': patient_data[8],
                    'obesity': patient_data[9],
                    'alcohol_consumption': patient_data[10],
                    'exercise_hours_per_week': patient_data[11],
                    'diet': patient_data[12],
                    'previous_heart_problems': patient_data[13],
                    'medication_use': patient_data[14],
                    'stress_level': patient_data[15],
                    'sedentary_hours_per_day': patient_data[16],
                    'income': patient_data[17],
                    'bmi': patient_data[18],
                    'triglycerides': patient_data[19],
                    'physical_activity_days_per_week': patient_data[20],
                    'sleep_hours_per_day': patient_data[21],
                    'country': patient_data[22],
                    'continent': patient_data[23],
                    'hemisphere': patient_data[24],
                    'heart_attack_risk': patient_data[25],
                    'status': patient_data[26],
                    'user_id': patient_data[27],
                    'sex': patient_data[28],
                    'created_at': self.__format_date(patient_data[29]),
                    'updated_at': self.__format_date(patient_data[30]),
                }
                list_patient_data.append(_patient_data)

        return list_patient_data


    def get_all_patient_data_df(self):
        import pandas as pd
        cur = self.conn.connection.cursor()
        cur.execute(self.QUERYS.SELECT_ALL_FROM.format('patient_data'))
        data = cur.fetchall()
        cur.close()

        columns_to_exclude = ['user_id', 'created_at', 'updated_at', 'status']

        list_patient_data = []

        if data:
            for patient_data in data:
                _patient_data = {
                    'patient_id': patient_data[1],
                    'age': patient_data[2],
                    'cholesterol': patient_data[3],
                    'blood_pressure': patient_data[4],
                    'heart_rate': patient_data[5],
                    'diabetes': patient_data[6],
                    'family_history': patient_data[7],
                    'smoking': patient_data[8],
                    'obesity': patient_data[9],
                    'alcohol_consumption': patient_data[10],
                    'exercise_hours_per_week': patient_data[11],
                    'diet': patient_data[12],
                    'previous_heart_problems': patient_data[13],
                    'medication_use': patient_data[14],
                    'stress_level': patient_data[15],
                    'sedentary_hours_per_day': patient_data[16],
                    'income': patient_data[17],
                    'bmi': patient_data[18],
                    'triglycerides': patient_data[19],
                    'physical_activity_days_per_week': patient_data[20],
                    'sleep_hours_per_day': patient_data[21],
                    'country': patient_data[22],
                    'continent': patient_data[23],
                    'hemisphere': patient_data[24],
                    'heart_attack_risk': patient_data[25],
                    'sex': patient_data[28],
                }
                list_patient_data.append(_patient_data)

            dataframe = pd.DataFrame(list_patient_data)
            return dataframe

    def add_patient_data(self, patient_id, age, cholesterol, blood_pressure, heart_rate, diabetes,
                         family_history, smoking, obesity, alcohol_consumption, exercise_hours_per_week,
                         diet, previous_heart_problems, medication_use, stress_level, sedentary_hours_per_day,
                         income, bmi, triglycerides, physical_activity_days_per_week, sleep_hours_per_day,
                         country, continent, hemisphere, heart_attack_risk, user_id, sex) -> None:
        cur = self.conn.connection.cursor()
        cur.execute(self.QUERYS.INSERT_INTO_PATIENT_DATA, (
            patient_id, age, cholesterol, blood_pressure, heart_rate,
            diabetes, family_history, smoking, obesity, alcohol_consumption,
            exercise_hours_per_week, diet, previous_heart_problems, medication_use,
            stress_level, sedentary_hours_per_day, income, bmi, triglycerides,
            physical_activity_days_per_week, sleep_hours_per_day, country, continent,
            hemisphere, heart_attack_risk, user_id, sex
        ))
        self.conn.connection.commit()
        cur.close()

    def delete_patient_data(self, patient_data_id) -> None:
        cur = self.conn.connection.cursor()
        cur.execute(
            self.QUERYS.DELETE_FROM.format(
                'patient_data', 'patient_data_id', patient_data_id
            )
        )
        self.conn.connection.commit()
        cur.close()

    def __format_date(self, date: str):
        if isinstance(date, str):
            fecha_objeto = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
        elif isinstance(date, datetime):
            fecha_objeto = date
        else:
            raise ValueError(
                "El argumento 'date' debe ser una cadena o un objeto datetime.")

        nuevo_formato = fecha_objeto.strftime("%Y-%m-%d %H:%M:%S")
        return nuevo_formato
