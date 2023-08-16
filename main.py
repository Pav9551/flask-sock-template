from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from random import random
from threading import Lock
from datetime import datetime
from flask_sock import Sock
import json

g_num = True
thread = None
thread_lock = Lock()

app = Flask(__name__)
socketio = SocketIO(app)

start_data = [
    {
        "101": {
            "status": "ok",
            "Уровень шума": "ok",
            "Температура": "ok",
            "Загазованность": "ok",
            "Размыкание цепей": "ok",
            "Протечки": "ok",
            "Активный заезд": "ok"
        }
    },
    {
        "102": {
            "status": "ok",
            "Уровень шума": "ok",
            "Температура": "ok",
            "Загазованность": "warning",
            "Размыкание цепей": "ok",
            "Протечки": "ok",
            "Активный заезд": "error"
        }
    }
]

start_data1 = [
    {
        "101": {
            "status": "ok",
            "Уровень шума": "ok",
            "Температура": "ok",
            "Загазованность": "ok",
            "Размыкание цепей": "ok",
            "Протечки": "ok",
            "Активный заезд": "ok"
        }
    },
    {
        "102": {
            "status": "ok",
            "Уровень шума": "ok",
            "Температура": "ok",
            "Загазованность": "warning",
            "Размыкание цепей": "ok",
            "Протечки": "ok",
            "Активный заезд": "ok"
        }
    }
]



def background_thread():
    print("Generating random sensor values")
    global g_num
    while True:
        print([i for i in start_data])
        g_num = not g_num
        print(g_num)
        if g_num:
            [socketio.emit('sensors', i) for i in start_data1]
        else:
            [socketio.emit('sensors', i) for i in start_data]
        socketio.sleep(1.0)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        json_data = json.loads(str(request.data, encoding='utf-8'))
        socketio.emit('sensors', json_data)
    return render_template('index.html')


@socketio.on('connect')
def test_message(message):
    print([i for i in start_data])
    # [emit('sensors', i) for i in start_data]
    global thread
    print('Client connected')
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
            pass



if __name__ == "__main__":
    socketio.run(app, port=3000, host='0.0.0.0')