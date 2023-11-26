from io import StringIO
from flask import make_response, jsonify, Blueprint, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from Models.DashboardModel import DashBoardModel
from Models.PatientDataModel import PatientDataModel
from Config.Config import Configuration
from DB.DB import DataBase
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.naive_bayes import GaussianNB
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.utils import class_weight
from imblearn.over_sampling import SMOTE


dash = Blueprint('dash', __name__)
app = DataBase().app

app = DataBase().app
dash_board = DashBoardModel()
patient_data_model = PatientDataModel()


@dash.route('/get_charts_data', methods=['GET'])
@cross_origin()
@jwt_required()
def get_charts_data():
    return make_response(jsonify({
        "chart1": dash_board.get_count_age(),
        "chart2": dash_board.get_count_sex(),
        "chart3": dash_board.get_count_smoking(),
        "chart4": dash_board.get_count_alcohol(),
        "chart5": dash_board.get_count_risk_hearth()
    }), 200)


@dash.route('/get_data_ml', methods=['GET'])
@cross_origin()
@jwt_required()
def get_data_ml():
    data = {}
    code = 200
    message = 'Data loaded successfully'

    try:
        df = patient_data_model.get_all_patient_data_df()
        is_null = df.isnull().any().any()

        # PASO 3 -> Limpieza de datos
        # PASO 3.1 -> Eliminar por algún método o no
        if is_null:
            # Op: llenar con moda
            df = df.fillna(df.mode().iloc[0])

        # Eliminar columnas irrelevantes
        columnas_irrelevantes = ['patient_id', 'country',
                                 'continent', 'hemisphere',
                                 'blood_pressure', 'diet']
        df = df.drop(columnas_irrelevantes, axis=1)

        # PASO 3.2 -> Convertir datos categóricos (como 'Sex') a numéricos usando one-hot encoding
        categorical_cols = ['sex']
        for col in categorical_cols:
            df = pd.get_dummies(df, columns=[col], drop_first=True)

        # PASO 3.3 -> Normalizar o estandarizar las columnas numéricas según sea necesario
        scaler = MinMaxScaler()  # o StandardScaler() según lo que prefieras
        columns_to_scale = ['age', 'cholesterol', 'heart_rate',
                            'exercise_hours_per_week', 'stress_level',
                            'bmi', 'triglycerides']
        df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

        # Obtener información del DataFrame
        buffer = StringIO()
        df.info(buf=buffer)
        info_result = buffer.getvalue()

        # Convertir información a una lista de diccionarios
        info_list = []
        for i, line in enumerate(info_result.split('\n')):
            words = line.split()
            if len(words) > 0:
                column_name = words[0]
                data_type = words[1] if len(words) > 1 else None
                info_dict = {'Index': i,
                             'Column': column_name, 'Type': data_type}
                info_list.append(info_dict)

        # PASO 4 -> Dividir el Conjunto de Datos
        # Definir las características (X) y la variable objetivo (y)
        X = df.drop('heart_attack_risk', axis=1)  # Features
        y = df['heart_attack_risk']  # Target variable

        # Dividir el conjunto de datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42)

        # PASO 5 -> Seleccionar y Entrenar un Modelo
        # Aplicar SMOTE para abordar el desequilibrio de clases
        smote = SMOTE(sampling_strategy=0.8, random_state=42, k_neighbors=3)
        X_train_resampled, y_train_resampled = smote.fit_resample(
            X_train, y_train)

        # Calcular los pesos de clase normalizados para el conjunto de datos equilibrado
        weights = class_weight.compute_class_weight(
            'balanced', classes=np.unique(y_train_resampled), y=y_train_resampled)

        # Normalizar los pesos de clase para que sumen 1
        weights = weights / np.sum(weights)

        # Definir los parámetros a ajustar
        param_grid = {'var_smoothing': [1e-1, 1e-5, 1e-9, 1e-12, 1e-15]}

        # Crear el modelo Naive Bayes
        modelo_naive_bayes = GaussianNB(priors=weights)

        # Configurar la búsqueda de hiperparámetros con validación cruzada
        grid_search = GridSearchCV(
            modelo_naive_bayes, param_grid, cv=5, scoring='accuracy')

        # Ajustar el modelo a los datos
        grid_search.fit(X_train_resampled, y_train_resampled)

        # Obtener el modelo con los mejores parámetros
        modelo_optimizado = grid_search.best_estimator_

        # Realizar predicciones y evaluar el rendimiento
        y_pred_optimizado = modelo_optimizado.predict(X_test)
        accuracy_optimizado = accuracy_score(y_test, y_pred_optimizado)

        # Obtener otras métricas como matriz de confusión y reporte de clasificación
        conf_matrix_optimizado = confusion_matrix(y_test, y_pred_optimizado)
        classification_rep_optimizado = classification_report(
            y_test, y_pred_optimizado, output_dict=True)

        # Convertir el classification_report a una lista de diccionarios
        classification_report_list = []
        for class_label, metrics in classification_rep_optimizado.items():
            if class_label in ['0', '1']:  # Adaptar según las etiquetas de tus clases
                class_metrics = {
                    'class_label': int(class_label),
                    'precision': metrics['precision'],
                    'recall': metrics['recall'],
                    'f1_score': metrics['f1-score'],
                    'support': metrics['support']
                }
                classification_report_list.append(class_metrics)

        # Componer el diccionario de respuesta
        data = {
            "dataframe_info": info_list[5:],
            "model_metrics": {
                "accuracy": accuracy_optimizado,
                "confusion_matrix": conf_matrix_optimizado.tolist(),
                "classification_report": classification_report_list
            }
        }

    except Exception as e:
        code = 400
        message = "Error: " + str(e)

    return make_response(
        jsonify(
            {"message": message, "data": data, "code": code}
        ), code)
