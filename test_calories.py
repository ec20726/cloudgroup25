from flask import Flask, jsonify, json, request
import requests 									#Requests library is used for external API calls

# sqlite is used as the lightwieght database to store our data, easy to use with python. Database name used in code is simply test.sqlite

import sqlite3

app = Flask(__name__)

# get request which allows someone to search the database for an excercise plan which matches the name passed to the function

@app.route('/exerciseplans/<name>', methods=['GET'])
def get_exerciseplan(name):

    conn = sqlite3.connect('test.sqlite')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    # temp_name needed due to the output of c.fetchall(). Tables shown as a list with a comma appended to their names.
    temp_name = name,
    
    # check if table already exists
    if temp_name in tables:
        sql_query = "SELECT * FROM '{}';".format(name)
        c.execute(sql_query)
        result = c.fetchall()
        return jsonify(result), 200
        
    else:
        return jsonify ({'error': 'Exercise plan not found!'}), 404

# get request which allows two variables to be passed to the function. Allows user to select individual exercises.

@app.route('/exerciseplans/<name>/<id>', methods=['GET'])
def get_exercise(name,id):
   
    conn = sqlite3.connect('test.sqlite')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    temp_name = name,
    
    if temp_name in tables:
        sql_query = "SELECT * FROM '{}' WHERE ID = '{}'".format(name,id)
        c.execute(sql_query)
        result = c.fetchall()
        if result == []:
            return jsonify ({'error': 'Sorry, this exercise does not exist!'}), 404

        else:
            return jsonify (result), 200
        
    else:
        return jsonify ({'error': 'Sorry, an exercise plan for this individual does not exist!'}), 404

# post request allowing a completly new user to create an exercise plan, this creates a new table in the sqlite database.

@app.route('/exerciseplans', methods=['POST'])
def post_exerciseplan():
    if not request.json or not 'name' in request.json:
        return jsonify({'error':'exercise plan needs a name'}), 400

    if request.json:
        individual = request.json
        data = individual["name"]
        conn = sqlite3.connect('test.sqlite')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        temp_name = data,

        if temp_name in tables:
            return jsonify ({'error': 'An exercise plan with this name already exists, please choose a different name'}), 409

        else:
            conn = sqlite3.connect('test.sqlite')
            c = conn.cursor()
            sql_query = "CREATE TABLE '{}' (id INTEGER PRIMARY KEY, sex TEXT NOT NULL, weight_kg REAL NOT NULL, height_cm REAL NOT NULL, age INTEGER NOT NULL, exercise TEXT, calories REAL);".format(data)
            c.execute(sql_query)
            conn.commit()
            return jsonify ({"message": "created:/exerciseplans/'{}'".format(data)}), 201

# post request where individual exercises are created with their own unique ID. This are inserted into the appropriate table in the database.

@app.route('/exerciseplans/<name>', methods=['POST'])
def post_exercise(name):

    conn = sqlite3.connect('test.sqlite')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    temp_name = name,

    if temp_name in tables:
        if not request.json or not request.json.keys() == {'sex','weight_kg','height_cm','age','exercise'}:
            return jsonify({'error':'Request must contain your sex, weight_kg, height_cm, age and the exercise'}), 400
        else:
            data = request.json
            #NUTRITIONIX API CALL START
            #nutritionix API endpoint
            url = "https://trackapi.nutritionix.com/v2/natural/exercise"

            #user details are concatenated into payload
            payload="{\"query\":\"" + data["exercise"] + "\", \"gender\":\"" + data["sex"] + "\", \"weight_kg\":" + str(data["weight_kg"]) + ", \"height_cm\":" + str(data["height_cm"]) + ", \"age\":" + str(data["age"]) +"}"

            #Headers include nutritionix developer id and key. user id of zero is used for development purposes.
            headers = {
             'x-app-id': '3a43bc4e',
              'x-remote-user-id': '0',
              'x-app-key': '4da5ae8742d7f84be4283a1bd832639c',
              'Content-Type': 'application/json'
            }

            #Response object is converted to json and the calorie estimate is stored in 'cal_response'
            response = requests.request("POST", url, headers=headers, data=payload)
            response_json = response.json()
            response_data = response_json["exercises"]
            response_dict = response_data[0]
            cal_response = response_dict["nf_calories"]
            #NUTRITIONIX API CALL END

            conn = sqlite3.connect('test.sqlite')
            c = conn.cursor()
            sql_query = "INSERT INTO '{}' VALUES (null, '{}', '{}', '{}', '{}', '{}', '{}');".format(name, data["sex"], data["weight_kg"], data["height_cm"], data["age"], data["exercise"], cal_response)
            c.execute(sql_query)
            conn.commit()
            sql_query_2 = "SELECT max(id) FROM '{}';".format(name)
            c.execute(sql_query_2)
            max_id = c.fetchone()[0]
            return jsonify ({"message": "created:/exerciseplans/'{}'/'{}".format(name, max_id)}), 201

    else:
        return jsonify ({'error': 'Exercise plan needs to be created for this individual first'}), 404

# delete request which allows a user to completly delete their exercise plan, this drops the table in sqlite with the name passed to the function.

@app.route('/exerciseplans/<name>', methods=['DELETE'])
def delete_exerciseplan (name):

    conn = sqlite3.connect('test.sqlite')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    temp_name = name,
    
    if temp_name in tables:
        sql_drop_table = "DROP TABLE '{}';".format(name)
        c.execute(sql_drop_table)
        conn.commit()
        return jsonify ({'message':'Exercise plan deleted'}), 200

    else:
        return jsonify ({'error': 'Sorry, an exercise plan for this individual does not exist!'}), 404

# delete request for individual exercises, this relates to the unique id which is created for each row in a users table.

@app.route('/exerciseplans/<name>/<id>', methods=['DELETE'])
def delete_exercise (name, id):

    conn = sqlite3.connect('test.sqlite')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    temp_name = name,
    
    if temp_name in tables:
        sql_query = "SELECT * FROM '{}' WHERE ID = '{}';".format(name,id)
        c.execute(sql_query)
        result = c.fetchall()
        blank = []
        if result == blank:
            return jsonify ({'error': 'ID does not exist!'}), 404

        else:
            sql_delete_query = "DELETE FROM '{}' WHERE ID = '{}';".format(name, id)
            c.execute(sql_delete_query)
            conn.commit()
            return jsonify ({'message':'Exercise deleted'}), 200
    
    else:
        return jsonify ({'error': 'Sorry, an exercise plan for this individual does not exist!'}), 404


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8090, debug=True)