from DB.DB import DataBase
from Tools.QueryTools import QueryTools
from datetime import datetime


class DashBoardModel(DataBase):

    QUERYS = QueryTools()

    def __init__(self):
        super().__init__()

    def get_count_sex(self) -> dict:
        cur = self.conn.connection.cursor()
        cur.execute(
            self.QUERYS.QUERY_COUNT_SEX
        )
        data = cur.fetchall()
        cur.close()

        labels_list = []
        label_data_list = []

        if data:
            print(data)
            for i in data:
                labels_list.append(i[1])
                label_data_list.append(i[0])

        return {"labels": labels_list,
                "label_data": label_data_list,
                "title": "Conteo de hombres y mujeres"}

    def get_count_age(self) -> dict:
        cur = self.conn.connection.cursor()
        cur.execute(
            self.QUERYS.QUERY_COUNT_AGE
        )
        data = cur.fetchall()
        cur.close()

        labels_list = []
        label_data_list = []

        if data:
            for i in data:
                labels_list.append(i[1])
                label_data_list.append(i[0])

        return {"labels": labels_list,
                "label_data": label_data_list,
                "title": "Conteo de edades"}

    def get_count_smoking(self) -> dict:
        cur = self.conn.connection.cursor()
        cur.execute(
            self.QUERYS.QUERY_COUNT_SMOKING
        )
        data = cur.fetchall()
        cur.close()

        labels_list = []
        label_data_list = []

        if data:
            for i in data:
                labels_list.append(i[1])
                label_data_list.append(i[0])

        return {"labels": labels_list,
                "label_data": label_data_list,
                "title": "Personas que fuman por sexo"}

    def get_count_alcohol(self) -> dict:
        cur = self.conn.connection.cursor()
        cur.execute(
            self.QUERYS.QUERY_COUNT_ALCOHOL
        )
        data = cur.fetchall()
        cur.close()

        labels_list = []
        label_data_list = []

        if data:
            for i in data:
                labels_list.append(i[1])
                label_data_list.append(i[0])

        return {"labels": labels_list,
                "label_data": label_data_list,
                "title": "Personas que consumen alcohol por sexo"}

    def get_count_risk_hearth(self) -> dict:
        cur = self.conn.connection.cursor()
        cur.execute(
            self.QUERYS.QUERY_COUNT_HEART_ATTACK_RISK
        )
        data = cur.fetchall()
        cur.close()

        labels_list = []
        label_data_list = []

        if data:
            for i in data:
                labels_list.append(i[1])
                label_data_list.append(i[0])

        return {"labels": labels_list,
                "label_data": label_data_list,
                "title": "Personas con riesgo de ataques cardiacos"}
