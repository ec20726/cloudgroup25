# cloudgroup25
Mini Project - Group 25

To view this app please visit: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com

This mini REST API enables the logging and tracking of user exercises. User details such as username, height and weight are stored and used for the calculation of calories burned during a user’s logged exercises. An exercise can be input to this REST API in the form of a single string e.g. ‘ran 10k’ and the Nutritionix API ( https://trackapi.nutritionix.com ) is then used to calculate the calories burnt. The exercise and its associated calories are then stored in the user’s exercise plan for future viewing. 

This REST API is built with Python and Flask and uses a MySQL database for data storage. This repo has been built to work with AWS Elastic Beanstalk to enable auto scaling of the application and uses a scalable MySQL database located outside of the Elastic beanstalk environment in AWS RDS.

For those wishing to set this app up, SQL code is provided at the bottom of this readme file to create the database tables and stored procedures needed for the running of this app.


## Using the API

### GET requests
To get all user details (no associated exercises) use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/userdetails

To get details for specific user (no associated exercises) use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/userdetails/username

To get all listed exercise (no associated user details) use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exercises

To get all user listed exercise for specific user (no associated user details) use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exercises/username

To get a specific exercise for user by exercise id (no associated user details) use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exercises/username/id

To get all exercise plans (users with associated exercises) use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans

To get exercise plan for specific user(user with associated exercises) use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans/username

#### Example of a curl GET requests for user's exercise plan:
curl --location --request GET 'http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans/bob'

### POST requests
To post a new user, use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans. New users can also be added through via the signup UI.

To post a new exercise for a specific user, use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans/username

#### Example of a curl POST request for a new user:
Note: All fields (firstname, lastname, username, height, weight, age and sex) are required. Height should be given in cm and weight in Kg.

curl --location --request POST 'http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans' --header 'Content-Type: application/json' --data-raw '{ "firstname": "Linda", "lastname": "Jones", "username": "linda123", "height": "183", "weight": "65", "age": "42", "sex": "Female" }'

#### Example of a curl POST request for adding a new exercise:
New exercises can be added for user through post requests to http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans/username. Any string can be used for the exercise as long as it makes logical sense, the Nutritionix API will sort out the rest !

curl --location --request POST 'http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans/carlo' --header 'Content-Type: application/json' --data-raw '{ "exercise" : "ran 10km" }'

### PUT requests
To update the user details (height, weight, username etc.) for a specific user, use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/userdetails

#### Example of a curl PUT request:
curl --location --request PUT 'http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/userdetails' --header 'Content-Type: application/json' --data-raw '{ "firstname": "Linda", "lastname": "Jones", "username": "linda123", "height": "187", "weight": "72", "age": "42", "sex": "Female" }'

### DELETE requests
To delete an exercise plan (user with associated exercises) for a specific user, use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans/username

To delete an exercise for a specific user, use: http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans/username/id

#### Example of a curl DELETE request:
curl --location --request DELETE 'http://flask-health-rest-api.eba-aq3hjvpm.us-east-2.elasticbeanstalk.com/exerciseplans/joey'

## If you are setting up a database for this app please use the following SQL:

To create the database
```
CREATE DATABDASE your_db_name;
```
To create the tables
```
-- -----------------------------------------------------
-- Table `your_db_name`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `your_db_name`.`users` (
  `user_username` VARCHAR(45) NOT NULL,
  `user_firstname` VARCHAR(45) NULL,
  `user_lastname` VARCHAR(45) NULL,
  `user_height` INT NULL,
  `user_weight` INT NULL,
  `user_age` INT NULL,
  `user_sex` VARCHAR(45) NULL,
  `user_date_created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `user_date_modified` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE INDEX `user_username_UNIQUE` (`user_username` ASC) VISIBLE,
  PRIMARY KEY (`user_username`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `your_db_name`.`exercises`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `your_db_name`.`exercises` (
  `exercise_id` INT NOT NULL AUTO_INCREMENT,
  `users_user_username` VARCHAR(45) NOT NULL,
  `exercise_type` VARCHAR(45) NULL,
  `exercise_calories_burned` INT NULL,
  `exercise_date_created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `exercise_date_modified` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`exercise_id`, `users_user_username`),
  UNIQUE INDEX `exercise_id_UNIQUE` (`exercise_id` ASC) VISIBLE,
  INDEX `fk_exercises_users_idx` (`users_user_username` ASC) VISIBLE,
  CONSTRAINT `fk_exercises_users`
    FOREIGN KEY (`users_user_username`)
    REFERENCES `your_db_name`.`users` (`user_username`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;
```
To create the stored procedure used in the UI form
```
DELIMITER $$
CREATE PROCEDURE `sp_createUser`(
    IN p_firstname VARCHAR(45),
    IN p_lastname VARCHAR(45),
    IN p_username VARCHAR(45),
    IN p_height INT,
    IN p_weight INT,
    IN p_age INT,
    IN p_sex VARCHAR(45)
)
BEGIN
    if ( select exists (select 1 from users where user_username = p_username) ) THEN
        select 'Sorry, this user name is already taken. Please pick another';
    ELSE
        insert into users
        (
            user_firstname,
            user_lastname,
            user_username,
            user_height,
            user_weight,
            user_age,
            user_sex
        )
        values
        (
            p_firstname,
            p_lastname,
            p_username,
            p_height,
            p_weight,
            p_age,
            p_sex

        );
    END IF;
END$$
DELIMITER ;
```


