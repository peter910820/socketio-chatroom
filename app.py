from flask import Flask, render_template
from flask_socketio import join_room, leave_room, SocketIO, send, emit

app = Flask(__name__, template_folder='./templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room/<string:room_name>')
def a(room_name):
    return render_template('room.html',room_name=room_name)

@socketio.on('connect')
def connect(auth):
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('join')
def handle_join(room_name):
    join_room(room_name)
    send(' has entered the room.', to=room_name)

@socketio.on('leave')
def handle_leave(room_name):
    leave_room(room_name)
    send(f'User has left the room.', to=room_name)


@socketio.on('message')
def handle_message(data: dict):
    room = data['room_id']
    msg = data['msg']
    send(msg, to=room)
    print('received message: ' + msg)
    # send(data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host='0.0.0.0', port=5000)