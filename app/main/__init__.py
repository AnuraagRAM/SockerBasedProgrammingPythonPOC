from flask import Flask, render_template
from flask_socketio import SocketIO, Namespace

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


from app.main.socket.indexsocket import PocSocketBasedProgramming

socketio.on_namespace(PocSocketBasedProgramming('/index'))

