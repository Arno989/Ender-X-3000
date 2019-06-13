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


# socket events
@socketio.on('connect')
def logConnect():
    print("connected")


@socketio.on('X')
def mvx(distance, direction):
    c = getcoords()
    if direction:
        value = distance + c[0]
    else:
        value = distance + c[0]
    serial.send_command({'command': 'G1 X' + str(value)})
    socketio.emit('ack')


@socketio.on('Y')
def mvy(distance, direction):
    c = getcoords()
    if direction:
        value = distance + c[1]
    else:
        value = distance + c[1]
    serial.send_command({'command': 'G1 Y' + str(value)})
    socketio.emit('ack')


@socketio.on('Z')
def mvz(distance, direction):
    c = getcoords()
    if direction:
        value = distance + c[2]
    else:
        value = distance + c[2]
    serial.send_command({'command': 'G1 Z' + str(value)})
    socketio.emit('ack')


@socketio.on('E')
def mve(distance, direction):
    c = getcoords()
    if direction:
        value = distance + c[3]
    else:
        value = distance + c[3]
    serial.send_command({'command': 'G1 E' + str(value)})
    socketio.emit('ack')


@socketio.on('xy-home')
def mvxyhome():
    serial.send_command({'command': 'G28 XY'})
    socketio.emit('ack')


@socketio.on('z-home')
def mvzhome():
    serial.send_command({'command': 'G28 Z'})
    socketio.emit('ack')


@socketio.on('motorsoff')
def motorsoff():
    serial.send_command({'command': 'M18'})
    socketio.emit('ack')


@socketio.on('fanon')
def fanon():
    serial.send_command({'command': 'M106 S255'})
    socketio.emit('ack')


@socketio.on('fanoff')
def fanoff():
    serial.send_command({'command': 'M107'})
    socketio.emit('ack')


def getcoords():
    return serial.send_command({'command': 'M114'})


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


# Start app
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
