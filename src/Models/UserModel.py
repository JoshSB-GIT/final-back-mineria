from DB.DB import DataBase
from Tools.QueryTools import QueryTools
from datetime import datetime


class UserModel(DataBase):
    QUERYS = QueryTools()

    def __init__(
        self, username: str = '', password: str = '',
        email: str = '', status=1
    ):
        super().__init__()
        self.username = username
        self.password = password
        self.email = email
        self.status = status

    def add_user(self) -> None:
        cur = self.conn.connection.cursor()
        cur.execute(
            self.QUERYS.INSERT_INTO_USERS,
            (self.username, self.password, self.email)
        )
        self.conn.connection.commit()
        cur.close()

    def get_all_users(self) -> list[dict]:
        cur = self.conn.connection.cursor()
        cur.execute(self.QUERYS.SELECT_ALL_FROM.format('users'))
        data = cur.fetchall()
        cur.close()

        list_user = []

        if data:
            for user in data:
                _user = {
                    'user_id': user[0],
                    'username': user[1],
                    'password': user[2],
                    'email': user[3],
                    'status': user[4],
                    'created_at': self.__format_date(user[5]),
                    'updated_at': self.__format_date(user[6]),
                }
                list_user.append(_user)

        return list_user

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

    def verify_user_credentials(self, email: str, password: str) -> dict:
        cur = self.conn.connection.cursor()
        cur.execute(
            self.QUERYS.SELECT_USER_LOGIN.format('users', email, password))
        data = cur.fetchone()
        cur.close()

        if data:
            return {"username": data[1], "email": data[3]}
        else:
            return {}
