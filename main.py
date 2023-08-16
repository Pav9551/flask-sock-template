from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from random import random
from threading import Lock
from datetime import datetime
from flask_sock import Sock
import json

g_num = 0
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
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
            "Активный заезд": "ok",
            "Устройство в сети": "error",
            "Счетчик": -1
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
            "Активный заезд": "error",
            "Устройство в сети": "error",
            "Счетчик": -1
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
            "Активный заезд": "ok",
            "Устройство в сети": "error",
            "Счетчик": -1
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
            "Активный заезд": "error",
            "Устройство в сети": "ok",
            "Счетчик": 10
        }
    }
]
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")
sock = Sock(app)

@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        if data == 'close':
            break
        ws.send(data)
        global g_num
        g_num = g_num + 1
        data = data.split()#разбиваем по пробелам
        if len(data) > 1:#если это не "connect", а ['57', '10']
            start_data1[1]['102']['Счетчик'] = data[0]
        [socketio.emit('sensors', i) for i in start_data1]


def background_thread():
    print("Generating random sensor values")
    global g_num
    while True:
        #print([i for i in start_data])
        #g_num = not g_num
        g_num = g_num - 1
        if g_num < 0:
            g_num = 0
        if g_num > 3:
            g_num = 3
        print(g_num)
        if g_num > 0:
            [socketio.emit('sensors', i) for i in start_data1]
        else:
            [socketio.emit('sensors', i) for i in start_data]
        socketio.sleep(0.2)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        json_data = json.loads(str(request.data, encoding='utf-8'))
        socketio.emit('sensors', json_data)
    return render_template('index.html')


@socketio.on('connect')
def test_message(message):
    #print([i for i in start_data])
    # [emit('sensors', i) for i in start_data]
    global thread
    print('Client connected')
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
            pass



if __name__ == "__main__":
    socketio.run(app, port=3000, host='0.0.0.0')