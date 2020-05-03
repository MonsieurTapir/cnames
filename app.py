from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "c2d4b1031c3cb671385a95ad84a2b99dc148cf8e0adf335a"
socketio = SocketIO(app,async_mode=None)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import views
import room_sockets

if __name__ == '__main__':
    app.run(debug=True)
