# cloudgroup25
Mini Project - Group 25

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
  `exercise_durration` INT NULL,
  `exercise_distance` INT NULL,
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


