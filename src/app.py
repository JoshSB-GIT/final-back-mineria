from flask import jsonify, request, make_response
from flask_cors import CORS, cross_origin
from Config.Config import config
from Routes.AuthRoutes import auth
from Routes.DashBoardRoutes import dash
from Routes.PatientDataRoutes import patient
from DB.DB import DataBase

app = DataBase.app
CORS(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(patient, url_prefix='/patient')
app.register_blueprint(dash, url_prefix='/dash')


@cross_origin
@app.route("/", methods=['GET', 'DELETE', 'POST', 'PUT'])
def home():
    if request.method == 'GET':
        return make_response(jsonify({'MESSAGE': "GET - HOME"}), 200)


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
