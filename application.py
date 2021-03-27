from flask import Flask, jsonify, json, request, render_template
# Requests library is used for external API calls
import requests 
# Flask's mySQL is used for database			                          
from flaskext.mysql import MySQL
# Required for security                                  
from werkzeug.security import generate_password_hash, check_password_hash


# variable named 'application' is required for AWS Elasticbeanstalk
# variable named 'app' is required by gunicorn
application = app = Flask(__name__) 
mysql = MySQL()


########################################################################################
### MySQL CONFIG
########################################################################################

app.config['MYSQL_DATABASE_USER']     = 'MYSQL_DATABASE_USER'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MYSQL_DATABASE_PASSWORD'
app.config['MYSQL_DATABASE_DB']       = 'MYSQL_DATABASE_DB'
app.config['MYSQL_DATABASE_HOST']     = 'MYSQL_DATABASE_HOST'
mysql.init_app(app)


########################################################################################
### TEMPLATE RENDERING
########################################################################################

# Get templates for pages with UI
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


########################################################################################
### UI SIGNUP FORM FUNCTIONALITY
########################################################################################

# POST method for UI form
@app.route('/signUp', methods=['POST'])
def signUp():
 
    # read values from form in signup.html
    firstname = request.form['inputFirstName']
    lastname  = request.form['inputLastName']
    username  = request.form['inputUsername']
    height    = request.form['inputHeight']
    weight    = request.form['inputWeight']
    age       = request.form['inputAge']
    sex       = request.form['inputSex']
 
    # call stored procedure in mysql database to create new users 
    # (only if username provided is unique)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc(
        'sp_createUser',
        (firstname,
        lastname,
        username,
        height,
        weight,
        age,
        sex)
        )
    data = cursor.fetchall()
    
    if len(data) == 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'}), 201
    else:
        return json.dumps({'error':str(data[0])}), 409


########################################################################################
### FORMATTING FUNCTIONS FOR JSON OUTPUT 
########################################################################################

def format_user_results(result):
    formated_results = []

    for row in result:
        result_dict = {}
        result_dict['username']      = row[0]
        result_dict['first_name']    = row[1]
        result_dict['last_name']     = row[2]
        result_dict['height']        = row[3]
        result_dict['weight']        = row[4]
        result_dict['age']           = row[5]
        result_dict['sex']           = row[6]
        result_dict['date_created']  = row[7]
        result_dict['date_modified'] = row[8]

        formated_results.append(result_dict)
    return formated_results

def format_ex_results(result):
    formated_results = []

    for row in result:
        result_dict = {}
        result_dict['username']        = row[0]
        result_dict['exercise_id']     = row[1]
        result_dict['exercise_type']   = row[2]
        result_dict['calories_burned'] = row[3]
        result_dict['date_created']    = row[4]
        result_dict['date_modified']   = row[5]

        formated_results.append(result_dict)
    return formated_results


########################################################################################
### MYSQL QUERY RUNNER FUNCTIONS
########################################################################################

# fetch query results
def run_sql_query(sql_query_str):
    conn = mysql.connect()
    c = conn.cursor()
    c.execute(sql_query_str)
    result = c.fetchall()
    return result

#commit query results
def run_sql_query_with_commit(sql_query_str):
    conn = mysql.connect()
    c = conn.cursor()
    c.execute(sql_query_str)
    conn.commit()
    result = c.fetchall()
    return result


########################################################################################
### FUNCTIONS FOR RUNNING SPECIFIC MYSQL QUERIES
########################################################################################

################################# QUERIES FOR GET ######################################

# Get all the users in the db
def get_all_users():

    return run_sql_query('SELECT * FROM users;')

# Get all the users in the db
def get_user_by_username(username):

    return run_sql_query(f"SELECT * FROM users WHERE user_username='{username}';")
    
# Get all exercises in the db
def get_all_exercises():

    query = (
        f"SELECT users_user_username, exercise_id, exercise_type,"
        f" exercise_calories_burned, exercise_date_created, exercise_date_modified"
        f" FROM exercises ORDER BY users_user_username;"
    )
    return run_sql_query(query)

# Get exercises for specific user
def get_all_exercises_for_user(username):

    query = (
        f"SELECT users_user_username, exercise_id, exercise_type,"
        f" exercise_calories_burned, exercise_date_created, exercise_date_modified"
        f" FROM exercises WHERE users_user_username='{username}';"
    )
    return run_sql_query(query)

def get_exercise_by_id_for_user(username, id):

    query = (
        f"SELECT users_user_username, exercise_id, exercise_type,"
        f" exercise_calories_burned, exercise_date_created, exercise_date_modified"
        f" FROM exercises WHERE users_user_username = '{username}'"
        f" AND exercise_id = '{id}'"
    )
    return run_sql_query(query)

def get_last_ex_id_for_user(username):

    query = (
        f"SELECT max(exercise_id) FROM exercises"
        f" WHERE users_user_username = '{username}';"
    )
    return run_sql_query(query)

################################# QUERIES FOR POST #####################################

def add_new_exercise(username, exercise, cal_response):

    query = (
        f"INSERT INTO exercises"
        f" (users_user_username, exercise_type, exercise_calories_burned)"
        f" VALUES ('{username}', '{exercise}', '{cal_response}');"
    )
    return run_sql_query_with_commit(query)

################################# QUERIES FOR PUT ######################################

def update_user_details(username, firstname, lastname, height, weight, age, sex):

    query = (
        f"UPDATE users SET user_username='{username}', user_firstname='{firstname}',"
        f" user_lastname='{lastname}', user_height='{height}',"
        f" user_weight='{weight}', user_age='{age}', user_sex='{sex}'"
        f" WHERE user_username = '{username}';"
    )
    return run_sql_query_with_commit(query)

################################ QUERIES FOR DELETE ####################################

def delete_user(username):

    query = (
        f"DELETE FROM users WHERE user_username = '{username}';"
    )
    return run_sql_query_with_commit(query)

def delete_exercise(username, id):

    query = (
        f"DELETE FROM exercises"
        f" WHERE users_user_username = '{username}' AND exercise_id = '{id}';"
    )
    return run_sql_query_with_commit(query)


########################################################################################
### GET METHODS FOR REST API
########################################################################################

# Show all users but only their account details (no associated exercises)
# In reality this should be protected so only admins could view it

@app.route('/userdetails', methods=['GET'])
def get_user_details():

    result = get_all_users()

    if result:
        return jsonify(format_user_results(result)), 200
    else:
        return jsonify ({'error': 'No users found!'}), 404

# Get user details for specified user
# In reality this should be protected so only the user logged in could view there details

@app.route('/userdetails/<username>', methods=['GET'])
def get_user_details_for_user(username):

    result = get_user_by_username(username)

    if result:
        return jsonify(format_user_results(result)), 200
    else:
        return jsonify ({'error': 'No user found with that username!'}), 404

# Show all exercises logged by all users

@app.route('/exercises', methods=['GET'])
def get_exercises():

    result = get_all_exercises()

    if result:
        formated_results = format_ex_results(result)
        return jsonify(formated_results), 200
    else:
        return jsonify ({'error': 'No exercises found!'}), 404

# Show all exercises logged by a specific user

@app.route('/exercises/<username>', methods=['GET'])
def get_exercises_for_user(username):

    result = get_all_exercises_for_user(username)

    if result:
        formated_results = format_ex_results(result)
        return jsonify(formated_results), 200
    else:
        return jsonify ({'error': 'No exercises can be found for this user!'}), 404

# Get request which allows two variables to be passed to the function. 
# Allows user to select individual exercises by username and exercise id.

@app.route('/exercises/<username>/<id>', methods=['GET'])
def get_exercise(username, id):
    
    result = get_exercise_by_id_for_user(username, id)

    if result:
        formated_results = format_ex_results(result)
        return jsonify (formated_results), 200
        
    else:
        return jsonify ({'error': 'This exercise or username does not exist!'}), 404

# Show all user excercise plans (account details + exercises)

@app.route('/exerciseplans', methods=['GET'])
def get_exerciseplans():

    users = get_all_users()
    formatted_users = format_user_results(users)
    
    if formatted_users:
        for user in formatted_users:
            user_ex = get_all_exercises_for_user(user['username'])
            formatted_user_ex = format_ex_results(user_ex)
            user['exercises_logged'] = formatted_user_ex

        return jsonify (formatted_users), 200
    else:
        return jsonify ({'error': 'Sorry, no users found !'}), 404


# Shows a single user excercise plan (account details + exercises)

@app.route('/exerciseplans/<username>', methods=['GET'])
def get_exerciseplan_for_user(username):
    
    user = get_user_by_username(username)
    formatted_user = format_user_results(user)

    if formatted_user:
        for user in formatted_user:
            user_ex = get_all_exercises_for_user(user['username'])
            formatted_user_ex = format_ex_results(user_ex)
            user['exercises_logged'] = formatted_user_ex
        return jsonify (formatted_user), 200
    else:
        return jsonify ({'error': 'Sorry, this username could not be found!'}), 404


########################################################################################
### POST METHODS FOR REST API
########################################################################################

# Post request allowing a completly new user to create an exercise plan 
# This creates a row in the mysql db table 'users'.

@app.route('/exerciseplans', methods=['POST'])
def post_exerciseplan():

    required = {'firstname','lastname','username','height','weight','age','sex'}
    if not request.json or not request.json.keys() == required:
            return jsonify({'error': f'Request must contain {required}'}), 400

    if request.json:
        user      = request.json
        firstname = user['firstname']
        lastname  = user['lastname']
        username  = user['username']
        height    = user['height']
        weight    = user['weight']
        age       = user['age']
        sex       = user['sex']

        conn = mysql.connect()
        cursor = conn.cursor()

        # uses a mysql stored procedure
        cursor.callproc(
            'sp_createUser',
            (firstname,
            lastname,
            username,
            height,
            weight,
            age,
            sex)
        )
        data = cursor.fetchall()
        
        if len(data) == 0:
            conn.commit()
            return jsonify ({"message": f"created:/exerciseplans/{username}"}), 201
        else:
            return jsonify ({'error': 'This username is already taken!'}), 409

# post request where individual exercises are created with their own unique ID. 
# This are inserted into the appropriate table in the database.

@app.route('/exerciseplans/<username>', methods=['POST'])
def post_exercise(username):

    result = get_user_by_username(username)
    user   = format_user_results(result)

    user_sex    = user[0]['sex']
    user_weight = user[0]['weight']
    user_height = user[0]['height']
    user_age    = user[0]['age']

    if user:
        if not request.json or not request.json.keys() == {'exercise'}:
            return jsonify({'error':'Request must contain the exercise'}), 400
        else:
            data = request.json
            #NUTRITIONIX API CALL START
            #nutritionix API endpoint
            url = "https://trackapi.nutritionix.com/v2/natural/exercise"

            # User details added for POST data
            params = {
                "query":data["exercise"],
                "gender":user_sex,
                "weight_kg":str(user_weight),
                "height_cm":str(user_height),
                "age":str(user_age)
            }
            payload = json.dumps(params)

            # Headers include nutritionix developer id and key. 
            # User id of zero is used for development purposes.
            headers = {
              'x-app-id': '3a43bc4e',
              'x-remote-user-id': '0',
              'x-app-key': '4da5ae8742d7f84be4283a1bd832639c',
              'Content-Type': 'application/json'
            }

            # Response object is converted to json
            # The calorie estimate is stored in 'cal_response'
            response      = requests.request("POST", url, headers=headers, data=payload)
            response_json = response.json()
            response_data = response_json["exercises"]
            response_dict = response_data[0]
            cal_response  = response_dict["nf_calories"]
            #NUTRITIONIX API CALL END

            add_new_exercise(username, data["exercise"], cal_response)
            new_id = get_last_ex_id_for_user(username)
            
            return jsonify ({"message": f"created:/exerciseplans/{username}/{new_id[0][0]}"}), 201

    else:
        return jsonify ({'error': 'This username does not exist !'}), 404


########################################################################################
### PUT METHODS FOR REST API
########################################################################################

# Update user details such as heigh, weight etc.

@app.route('/userdetails', methods=['PUT'])
def update_user():
    
    required = {'firstname','lastname','username','height','weight','age','sex'}
    if not request.json or not request.json.keys() == required:
            return jsonify({'error': f"Request must contain {required}"}), 400
    else:
        user      = request.json
        firstname = user['firstname']
        lastname  = user['lastname']
        username  = user['username']
        height    = user['height']
        weight    = user['weight']
        age       = user['age']
        sex       = user['sex']

        result = get_user_by_username(username)

        if result:
            update_user_details(
                username,
                firstname,
                lastname,
                height,
                weight,
                age,
                sex
            )

            return jsonify ({"message": f"updated:/exerciseplans/{username}"}), 201
        else:
            return jsonify ({'error': 'No user found with that username!'}), 404
        
    

########################################################################################
### DELETE METHODS FOR REST API
########################################################################################

# Delete request which allows a user to completly delete their exercise plan.
# This drops the user row in mysql 'users' table

@app.route('/exerciseplans/<username>', methods=['DELETE'])
def delete_exerciseplan (username):

    result = get_user_by_username(username)

    if result:
        delete_user(username)
        return jsonify ({'message':'User and exercise plan deleted'}), 200
    else:
        return jsonify ({'error': 'No user found with that username!'}), 404

  
# Delete request for individual exercises.
# This drops the exercise row for that user in mysql 'exercises' table

@app.route('/exerciseplans/<username>/<id>', methods=['DELETE'])
def delete_exercise_for_user (username, id):

    result = get_exercise_by_id_for_user(username, id)

    if result:
        delete_exercise(username, id)
        return jsonify ({'message':'Exercise deleted'}), 200
    else:
        return jsonify ({'error': 'This exercise or username does not exist!'}), 404


########################################################################################
### RUN APP
########################################################################################

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8090,  debug=True)
