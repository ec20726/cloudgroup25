from flask import Flask, jsonify, json, request, render_template
import requests 									                          # Requests library is used for external API calls
from flaskext.mysql import MySQL                                              # Flask's mySQL is used for database
from werkzeug.security import generate_password_hash, check_password_hash     # Will be used for SHA password hashing


# variable named 'application' is required for AWS Elasticbeanstalk, 'app' required by 
application = app = Flask(__name__) 

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER']     = 'MYSQL_DATABASE_USER'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MYSQL_DATABASE_PASSWORD'
app.config['MYSQL_DATABASE_DB']       = 'MYSQL_DATABASE_DB'
app.config['MYSQL_DATABASE_HOST']     = 'MYSQL_DATABASE_HOST'
mysql.init_app(app)

# Get templates for pages with UI
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# POST method for UI form
@app.route('/signUp', methods=['POST'])
def signUp():
 
    # read values from form in signup.html
    _firstname = request.form['inputFirstName']
    _lastname  = request.form['inputLastName']
    _username  = request.form['inputUsername']
    _height    = request.form['inputHeight']
    _weight    = request.form['inputWeight']
    _age       = request.form['inputAge']
    _sex       = request.form['inputSex']
 
    # validate the received values
    if not _firstname and _lastname and _username:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

    # call stored procedure in mysql database to create new users (only if username provided is unique)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc(
        'sp_createUser',
        (_firstname,
        _lastname,
        _username,
        _height,
        _weight,
        _age,
        _sex)
        )
    data = cursor.fetchall()
    
    if len(data) == 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})

def format_resulrs_for_JSON(result):
    formated_results = []

    for row in result:
        result_dict = {}
        result_dict['exercise_id']     = row[0]
        result_dict['exercise_type']   = row[1]
        result_dict['calories_burned'] = row[2]
        result_dict['date_created']    = row[3]
        result_dict['date_modified']   = row[4]
        formated_results.append(result_dict)
    return formated_results

# get request which allows someone to search the database for an excercise plan which matches the name passed to the function
@app.route('/exerciseplans/<username>', methods=['GET'])
def get_exerciseplan(username):

    conn = mysql.connect()
    c = conn.cursor()
    sql_query = 'SELECT exercise_id,exercise_type,exercise_calories_burned,exercise_date_created,exercise_date_modified FROM exercises WHERE users_user_username="{}";'.format(username)
    c.execute(sql_query)
    result = c.fetchall()
    
    if result:
        formated_results = format_resulrs_for_JSON(result)
        return jsonify(formated_results), 200
    else:
        return jsonify ({'error': 'Exercise plan not found!'}), 404
    

# get request which allows two variables to be passed to the function. Allows user to select individual exercises.
@app.route('/exerciseplans/<username>/<id>', methods=['GET'])
def get_exercise(username, id):
   
    conn = mysql.connect()
    c = conn.cursor()
    sql_query = "SELECT exercise_id,exercise_type,exercise_calories_burned,exercise_date_created,exercise_date_modified FROM exercises WHERE users_user_username = '{}' AND exercise_id = '{}'".format(username, id)
    c.execute(sql_query)
    result = c.fetchall()

    if result:
        formated_results = format_resulrs_for_JSON(result)
        return jsonify (formated_results), 200
        
    else:
        return jsonify ({'error': 'Sorry, this exercise does not exist or an exercise plan for this individual does not exist!'}), 404


# post request allowing a completly new user to create an exercise plan, this creates a row in the mysql db.
@app.route('/exerciseplans', methods=['POST'])
def post_exerciseplan():
    if not request.json:
        return jsonify({'error':'No JSON request'}), 400

    if not request.json or not request.json.keys() == {'firstname','lastname','username','height','weight','age','sex'}:
            return jsonify({'error':'Request must contain your first name, last name, username, height, weight, age and sex'}), 400

    if request.json:
        individual = request.json
        _firstname = individual['firstname']
        _lastname  = individual['lastname']
        _username  = individual['username']
        _height    = individual['height']
        _weight    = individual['weight']
        _age       = individual['age']
        _sex       = individual['sex']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc(
            'sp_createUser',
            (_firstname,
            _lastname,
            _username,
            _height,
            _weight,
            _age,
            _sex)
        )
        data = cursor.fetchall()
        
        if len(data) == 0:
            conn.commit()
            return jsonify ({"message": "created:/exerciseplans/{}".format(_username)}), 201
        else:
            return jsonify ({'error': 'This username is already taken! please choose a different username'}), 409

# Update user details such as heigh, weight etc.
# @app.route('/exerciseplans', methods=['PUT'])
# def post_exerciseplan():
#     if not request.json:
#         return jsonify({'error':'No JSON request'}), 400

#     if not request.json or not request.json.keys() == {'firstname','lastname','username','height','weight','age','sex'}:
#             return jsonify({'error':'Request must contain your first name, last name, username, height, weight, age and sex'}), 400

#     if request.json:
#         individual = request.json
#         _firstname = individual['firstname']
#         _lastname  = individual['lastname']
#         _username  = individual['username']
#         _height    = individual['height']
#         _weight    = individual['weight']
#         _age       = individual['age']
#         _sex       = individual['sex']

#         conn = mysql.connect()
#         cursor = conn.cursor()

# post request where individual exercises are created with their own unique ID. This are inserted into the appropriate table in the database.
@app.route('/exerciseplans/<username>', methods=['POST'])
def post_exercise(username):

    conn = mysql.connect()
    c = conn.cursor()
    sql_query = "SELECT user_sex,user_weight,user_height,user_age FROM users WHERE user_username = '{}';".format(username)
    c.execute(sql_query)
    user = c.fetchall()
    
    user_sex = user[0][0]
    user_weight = user[0][1]
    user_height = user[0][2]
    user_age = user[0][3]

    # return jsonify(user_age)
    if user:
        if not request.json or not request.json.keys() == {'exercise'}:
            return jsonify({'error':'Request must contain the exercise'}), 400
        else:
            data = request.json
            #NUTRITIONIX API CALL START
            #nutritionix API endpoint
            url = "https://trackapi.nutritionix.com/v2/natural/exercise"

            #user details are concatenated into payload
            payload="{\"query\":\"" + data["exercise"] + "\", \"gender\":\"" + user_sex + "\", \"weight_kg\":" + str(user_weight) + ", \"height_cm\":" + str(user_height) + ", \"age\":" + str(user_age) +"}"

            #Headers include nutritionix developer id and key. user id of zero is used for development purposes.
            headers = {
             'x-app-id': '3a43bc4e',
              'x-remote-user-id': '0',
              'x-app-key': '4da5ae8742d7f84be4283a1bd832639c',
              'Content-Type': 'application/json'
            }

            #Response object is converted to json and the calorie estimate is stored in 'cal_response'
            response      = requests.request("POST", url, headers=headers, data=payload)
            response_json = response.json()
            response_data = response_json["exercises"]
            response_dict = response_data[0]
            cal_response  = response_dict["nf_calories"]
            #NUTRITIONIX API CALL END

            conn = mysql.connect()
            c = conn.cursor()
            sql_query = "INSERT INTO exercises (users_user_username, exercise_type, exercise_calories_burned) VALUES ('{}', '{}', '{}');".format(username, data["exercise"], cal_response)
            c.execute(sql_query)
            conn.commit()
            sql_query_new_ex_id = "SELECT max(exercise_id) FROM exercises WHERE users_user_username = '{}';".format(username)
            c.execute(sql_query_new_ex_id)
            new_id = c.fetchone()[0]
            return jsonify ({"message": "created:/exerciseplans/{}/{}".format(username, new_id)}), 201

    else:
        return jsonify ({'error': 'This username does not exist. Exercise plan needs to be created for this individual first'}), 404

# delete request which allows a user to completly delete their exercise plan, this drops the user row in mysql user table
@app.route('/exerciseplans/<username>', methods=['DELETE'])
def delete_exerciseplan (username):

    conn = mysql.connect()
    c = conn.cursor()
    sql_delete_user = "DELETE FROM users WHERE user_username = '{}';".format(username)
    c.execute(sql_delete_user)
    conn.commit()
    return jsonify ({'message':'Exercise plan deleted'}), 200
  

# delete request for individual exercises.
@app.route('/exerciseplans/<username>/<id>', methods=['DELETE'])
def delete_exercise (username, id):

    conn = mysql.connect()
    c = conn.cursor()
    sql_delete_query = "DELETE FROM exercises WHERE users_user_username = '{}' AND exercise_id = '{}';".format(username, id)
    c.execute(sql_delete_query)
    conn.commit()
    return jsonify ({'message':'Exercise deleted'}), 200

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8090,  debug=True)
