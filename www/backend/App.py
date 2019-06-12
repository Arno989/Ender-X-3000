# Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO

from modules.SensorReadings import Sensor
from modules.Serialcom import Serialcom
from modules.DatabaseConn import Database

# Start app and socket
app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

# Connect to database
conn = Database(app=app, user='sensoruser', password='sensoruser', db='site')
# Initialise serial communication
serial = Serialcom()
# Initialise sersor reading
sensors = Sensor(conn, serial)
# Custom endpoint
endpoint = '/api/v1'


# ROUTES
@app.route(endpoint + '/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        try:
            result = request.get_json()
            user_username = result['username']
            user_password = result['password']

            added_user_id = conn.set_data("INSERT INTO user (username, password) VALUES (%s, %s)", [user_username, user_password])
            return jsonify(userID=added_user_id), 201

        except Exception as e:
            return jsonify(error=Exception), 400

    if request.method == 'GET':
        try:
            result = conn.get_data("SELECT username FROM user")
            return jsonify(result), 200
        except:
            return jsonify(error=Exception), 400


@app.route(endpoint + '/users/<username>', methods=['GET', 'PUT', 'DELETE'])
def user(username):
    if request.method == 'GET':
        try:
            result = conn.get_data("SELECT * FROM user where username = (%s)", username)
            return jsonify(result), 200
        except:
            return jsonify(error=Exception), 400


@app.route(endpoint + '/data/printer/temp', methods=['GET'])
def printerTemp():
    if request.method == 'GET':
        try:
            # result = conn.get_data("SELECT * FROM (SELECT * FROM printertemp ORDER BY timestamp DESC LIMIT 11) SQ ORDER BY timestamp ASC LIMIT 11;")
            result = conn.get_data(
                "SELECT * FROM (SELECT * FROM data WHERE sensor = 'th' ORDER BY timestamp DESC LIMIT 11) SQ UNION SELECT * FROM (SELECT * FROM data WHERE sensor = 'ta' ORDER BY timestamp DESC LIMIT 11) SQ UNION SELECT * FROM (SELECT * FROM data WHERE sensor = 'tb' ORDER BY timestamp DESC LIMIT 11) SQ ORDER BY timestamp ASC;")
            return jsonify(result), 200
        except:
            return jsonify(error=Exception), 400


@app.route(endpoint + '/data/humid', methods=['GET'])
def printerHumid():
    if request.method == 'GET':
        try:
            result = conn.get_data(
                "SELECT * FROM (SELECT * FROM data WHERE sensor = 'hp' ORDER BY timestamp DESC LIMIT 100) SQ UNION SELECT * FROM (SELECT * FROM data WHERE sensor = 'hf' ORDER BY timestamp DESC LIMIT 100) SQ ORDER BY timestamp ASC;")
            return jsonify(result), 200
        except:
            return jsonify(error=Exception), 400


@app.route(endpoint + '/data/printer/gas', methods=['GET'])
def printerGas():
    if request.method == 'GET':
        try:
            result = conn.get_data(
                "SELECT * FROM (SELECT * FROM data WHERE sensor = 'co2' ORDER BY timestamp DESC LIMIT 100) SQ UNION SELECT * FROM (SELECT * FROM data WHERE sensor = 'tvo' ORDER BY timestamp DESC LIMIT 100) SQ ORDER BY timestamp ASC;")
            return jsonify(result), 200
        except:
            return jsonify(error=Exception), 400


@app.route(endpoint + '/data/fillament/temp', methods=['GET'])
def fillamentTemp():
    if request.method == 'GET':
        try:
            result = conn.get_data("SELECT * FROM (SELECT * FROM data WHERE sensor = 'tf' ORDER BY timestamp DESC LIMIT 100) SQ ORDER BY timestamp ASC;")
            return jsonify(result), 200
        except:
            return jsonify(error=Exception), 400


# socket events
@socketio.on('connect')
def logConnect():
    print("connected")


@socketio.on('xy-up')
def mvxyup(distance):
    serial.send_command({'command': 'G1', 'axis': 'y', 'value': distance})
    socketio.emit('ack')


@socketio.on('xy-left')
def mvxyleft(distance):
    serial.send_command({'command': 'G1', 'axis': 'x', 'value': distance, 'negative': True})
    socketio.emit('ack')


@socketio.on('xy-home')
def mvxyhome(distance):
    serial.send_command({'command': 'G28', 'axis': 'xy', 'value': distance})
    socketio.emit('ack')


@socketio.on('xy-right')
def mvxyright(distance):
    serial.send_command({'command': 'G1', 'axis': 'x', 'value': distance})
    socketio.emit('ack')


@socketio.on('xy-down')
def mvxydown(distance):
    serial.send_command({'command': 'G1', 'axis': 'y', 'value': distance, 'negative': True})
    socketio.emit('ack')


@socketio.on('z-up')
def mvzup(distance):
    serial.send_command({'command': 'G1', 'axis': 'z', 'value': distance})
    socketio.emit('ack')


@socketio.on('z-home')
def mvzhome(distance):
    serial.send_command({'command': 'G28', 'axis': 'z', 'value': distance})
    socketio.emit('ack')


@socketio.on('z-down')
def mvzdown(distance):
    serial.send_command({'command': 'G1', 'axis': 'z', 'value': distance, 'negative': True})
    socketio.emit('ack')


@socketio.on('extrude')
def extrude(value):
    serial.send_command({'command': 'G1', 'axis': 'e', 'value': value})
    socketio.emit('ack')


@socketio.on('retract')
def retract(value):
    serial.send_command({'command': 'G1', 'axis': 'e', 'value': value, 'negative': True})
    socketio.emit('ack')


@socketio.on('motorsoff')
def motorsoff():
    serial.send_command({'command': 'M18'})
    socketio.emit('ack')


@socketio.on('fanon')
def fanon():
    serial.send_command({'command': 'M106'})
    socketio.emit('ack')


@socketio.on('fanoff')
def fanoff():
    serial.send_command({'command': 'M107'})
    socketio.emit('ack')


# Start app
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
