from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # It helps to encrypt the session data
app.config['DEBUG'] = True

"""
    Run Flask app in Socket.io
    async_mode help to pick one from the model. Valid async modes are threading, eventlet, gevent and gevent_uwsgi.
    It it is not mentioned it pick in from the hierarchy eventlet is tried first,
        then gevent_uwsgi, then gevent, and finally threading
    Logger for logging
"""
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


from app.main.socket.indexsocket import PocSocketBasedProgramming

socketio.on_namespace(PocSocketBasedProgramming('/index'))

