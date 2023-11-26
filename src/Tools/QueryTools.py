class QueryTools():
    SELECT_ALL_FROM = "SELECT * FROM {} WHERE status = '1'"
    SELECT_USER_LOGIN = "SELECT * FROM {} WHERE email = '{}' AND password = '{}' AND status = '1'"

    INSERT_INTO_USERS = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    INSERT_INTO_PATIENT_DATA = """
            INSERT INTO patient_data (
                patient_id, age, cholesterol, blood_pressure, heart_rate, diabetes,
                family_history, smoking, obesity, alcohol_consumption, exercise_hours_per_week,
                diet, previous_heart_problems, medication_use, stress_level,
                sedentary_hours_per_day, income, bmi, triglycerides,
                physical_activity_days_per_week, sleep_hours_per_day, country,
                continent, hemisphere, heart_attack_risk, user_id, sex
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

    DELETE_FROM = "DELETE FROM {} WHERE {}={}"

    # CONTAR - Cantidad de personas de cada sexo
    QUERY_COUNT_SEX = """
        SELECT
            COUNT(pd.sex) AS CANTIDAD,
            IF(pd.sex = 1, 'Female', 'Male') AS NAME 
        FROM
            patient_data AS pd 
        GROUP BY
            pd.sex;
    """

    # Cantidad de personas de cada edad
    QUERY_COUNT_AGE = """
        SELECT
            COUNT(pd.age) AS CANTIDAD,
            pd.age
        FROM
            patient_data AS pd 
        GROUP BY
            pd.age;
    """

    # Cantidad de personas que fuman de cada sexo
    QUERY_COUNT_SMOKING = """
        SELECT
            COUNT(*) AS CANTIDAD,
            IF(pd.sex = 1, 'Female', 'Male') AS NAME 
        FROM
            patient_data AS pd
        WHERE
            pd.smoking = 1
        GROUP BY
            pd.sex;
    """

    # Cantidad de personas con obesidad de cada sexo
    QUERY_COUNT_OBESITY = """
        SELECT
            COUNT(*) AS CANTIDAD,
            IF(pd.sex = 1, 'Female', 'Male') AS NAME 
        FROM
            patient_data AS pd
        WHERE
            pd.obesity = 1
        GROUP BY
            pd.sex;
    """

    # Cantidad de personas que consumen alcohol de cada sexo
    QUERY_COUNT_ALCOHOL = """
        SELECT
            COUNT(*) AS CANTIDAD,
            IF(pd.sex = 1, 'Female', 'Male') AS NAME 
        FROM
            patient_data AS pd
        WHERE
            pd.alcohol_consumption = 1
        GROUP BY
            pd.sex;
    """

    # Cantidad de personas con riesgo de ataque al corazón
    QUERY_COUNT_HEART_ATTACK_RISK = """
        SELECT
            COUNT(*) AS CANTIDAD,
            pd.heart_attack_risk
        FROM
            patient_data AS pd
        GROUP BY
            pd.heart_attack_risk;
    """
