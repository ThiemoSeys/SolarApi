from flask import Flask

from scripts.dbManager import *

app = Flask(__name__)
manager = dbManager()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
