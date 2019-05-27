# Imports
from flask import Flask, jsonify, request, url_for, json
from flask_cors import CORS

# Custom imports
from database import Database

# Start app
app = Flask(__name__)
CORS(app)

conn = Database(app=app, user='root', password='root', db='site')

# Custom endpoint
endpoint = '/api/v1'


# ROUTES
@app.route(endpoint + '/')
def index():
        return 'index'

@app.route(endpoint + '/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        try:
            result = request.get_json()
            print(result)
            user_username = result['username']
            user_password = result['password']

            added_user_id = conn.set_data("INSERT INTO user (username, password) VALUES (%s, %s)", [user_username, user_password])
            return jsonify(userID = added_user_id), 201

        except Exception as e:
            return jsonify(error=Exception), 400

    if request.method == 'GET':
        try:
            result = conn.get_data("SELECT username FROM user")
            return jsonify(result), 200
        except :
            return jsonify(error=Exception), 400

@app.route(endpoint + '/users/<username>',  methods=['GET', 'PUT', 'DELETE'])
def user(username):
    if request.method == 'GET':
        try:
            result = conn.get_data("SELECT * FROM user where username = (%s)", username)
            return jsonify(result), 200
        except :
            return jsonify(error=Exception), 400



@app.route(endpoint + '/data/printer/temp',  methods=['GET'])
def printerTemp():
    if request.method == 'GET':
        try:
            result = conn.get_data("SELECT * FROM (SELECT * FROM printertemp ORDER BY timestamp DESC LIMIT 11) SQ ORDER BY timestamp ASC LIMIT 11;")
            print("result")
            return jsonify(result), 200
        except :
            return jsonify(error=Exception), 400

@app.route(endpoint + '/data/humid',  methods=['GET'])
def printerHumid():
    if request.method == 'GET':
        try:
            result = conn.get_data("SELECT * FROM humidity")
            return jsonify(result), 200
        except :
            return jsonify(error=Exception), 400

@app.route(endpoint + '/data/printer/gas',  methods=['GET'])
def printerGas():
    if request.method == 'GET':
        try:
            result = conn.get_data("SELECT * FROM printerGas")
            return jsonify(result), 200
        except :
            return jsonify(error=Exception), 400

@app.route(endpoint + '/data/fillament/temp',  methods=['GET'])
def fillamentTemp():
    if request.method == 'GET':
        try:
            result = conn.get_data("SELECT * FROM fillamentTemp")
            return jsonify(result), 200
        except :
            return jsonify(error=Exception), 400

# Start app
if __name__ == '__main__':
    app.run(debug=True)



'''
    elif request.method == 'PUT':
        try:
            user_update = request.get_json()

            user_password = user_update['password']

            updated_user_id = \
                conn.set_data("UPDATE user set password = %s WHERE username = %s", [user_password, username])
            return jsonify('train data updated ', updated_user_id), 200
        except:
            return jsonify(error=Exception), 400

    elif request.method == "DELETE":
        try:
            changed_rows = conn.delete_data("DELETE FROM user WHERE username = %s", username)
            if username == "":
                return jsonify(Deleted="No records were deleted"), 204
            else:
                return jsonify(Deleted="{0} records deleted".format(changed_rows)), 201
        except:
            return jsonify(error=Exception), 400

'''