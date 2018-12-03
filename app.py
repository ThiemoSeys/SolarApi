import json

from flask import Flask

from scripts.dbManager import *

logging.basicConfig(level=logging.DEBUG, filename="log_flask.txt")


app = Flask(__name__)
manager = dbManager()


@app.route('/')
def hello_world():
    return 'Welcome to my SolarApi, the useable endpoints are.....!'


@app.route('/station/<setup>')
def show_user_profile(setup):
    try:
        data = manager.read_data_from_solar(setup)
        data = json.dumps(data)
    except ValueError as e:
        print(e)
    return data



if __name__ == '__main__':
    app.run()
