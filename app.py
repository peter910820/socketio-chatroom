from flask import Flask
from flask import make_response, render_template, request
from flask_socketio import SocketIO
from flask_socketio import emit, join_room, send

app = Flask(__name__, template_folder='./templates')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room/<string:room_name>', methods=["POST"])
def handler(room_name):
    resp = make_response(render_template('room.html', room_name = request.form["roomnumber"], username = request.form["username"]))
    resp.set_cookie('username', request.form["username"])
    return resp

@socketio.on('connect')
def connect():
    print('Client connect')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnect')

@socketio.on('join')
def handle_join(room_name, username):
    join_room(room_name)
    emit('join', f'{username} jump into {room_name}', to=room_name)

@socketio.on('message')
def handle_message(data: dict):
    room = data['room_id']
    msg = data['msg']
    username = data['username']
    send({'msg': msg, 'username': username}, to=room)
    print('received message: ' + msg)
    # send(data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host='0.0.0.0', port=5000)