# Tutor-Bird
Team 77: Junjie Lin, Charles Chu, Shiyou Yan, Zinan Guo


Table Definition: 
CREATE TABLE user (
  user_id int(11) NOT NULL AUTO_INCREMENT,
  user_firstname varchar(255) CHARACTER SET utf8 NOT NULL,
  user_lastname varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  user_dob date DEFAULT NULL,
  user_email varchar(255) CHARACTER SET utf8 NOT NULL,
  user_phoneNum bigint(20) DEFAULT NULL,
  user_username varchar(255) CHARACTER SET utf8 NOT NULL,
  user_password varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  user_joinDate date NOT NULL,
  user_availability varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  user_role varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (user_id)
) 

CREATE TABLE tutor (
  tutor_id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  teach_course varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  about_me varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (tutor_id),
  KEY user_id (user_id)
) 
CREATE TABLE student (
  student_id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  help_course varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (student_id),
  KEY user_id (user_id)
) 
CREATE TABLE staff (
  staff_id int(11) NOT NULL,
  user_id int(11) NOT NULL,
  role varchar(255) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (staff_id),
  KEY user_id (user_id)
) 

CREATE TABLE session (
  session_id int(11) NOT NULL,
  student_id int(11) NOT NULL,
  tutor_id int(11) NOT NULL,
  session_when datetime NOT NULL,
  session_link varchar(255) CHARACTER SET utf8 NOT NULL,
  student_feedback varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  tutor_feedback varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (session_id),
  KEY student_id (student_id),
  KEY tutor_id (tutor_id)
) 

CREATE TABLE course ( 

    course_id INT PRIMARY KEY, 

    teach_course VARCHAR(255) 

); 

INSERT INTO Course (course_id, teach_course)  

VALUES (1, 'Biology'); 

INSERT INTO Course (course_id, teach_course)  

VALUES (2, 'Chinese'); 
 
INSERT INTO Course (course_id, teach_course)  

VALUES (3, 'World History'); 
 
INSERT INTO Course (course_id, teach_course)  

VALUES (4, 'Mathematics'); 

INSERT INTO Course (course_id, teach_course)  

VALUES (5, 'Government'); 

INSERT INTO Course (course_id, teach_course)  

VALUES (6, 'Geography'); 

INSERT INTO Course (course_id, teach_course)  

VALUES (7, 'Literature'); 

INSERT INTO Course (course_id, teach_course)  

VALUES (8, 'Chemistry'); 

INSERT INTO Course (course_id, teach_course)  

VALUES (9, 'Physics'); 

CREATE TABLE Period ( 

    period_id INT PRIMARY KEY, 

    time_slot VARCHAR(255) 

); 

INSERT INTO Period (period_id, time_slot)  

VALUES (1, '9:00-10:00'); 

INSERT INTO Period (period_id, time_slot)  

VALUES (2, '10:00-11:00');  

INSERT INTO Period (period_id, time_slot)  

VALUES (3, '11:00-12:00'); 

INSERT INTO Period (period_id, time_slot)  

VALUES (4, '12:00-13:00'); 

INSERT INTO Period (period_id, time_slot)  

VALUES (5, '13:00-14:00');

INSERT INTO Period (period_id, time_slot)  

VALUES (6, '14:00-15:00'); 

INSERT INTO Period (period_id, time_slot)  

VALUES (7, '15:00-16:00'); 

CREATE TABLE Schedule ( 

    schedule_id INT PRIMARY KEY, 

    tutor_id INT, 

    course_id INT, 

    day_of_week VARCHAR(255), 

    period_id INT 

); 

 

 

ALTER TABLE Tutor ENGINE = InnoDB; 

ALTER TABLE Schedule 

ADD FOREIGN KEY (tutor_id) REFERENCES tutor(tutor_id), 

ADD FOREIGN KEY (course_id) REFERENCES Course(course_id), 

ADD FOREIGN KEY (period_id) REFERENCES Period(period_id); 

  

CREATE TABLE Days  

( day_id INT PRIMARY KEY,  

day_name VARCHAR(255) ); 

 

INSERT INTO Days (day_id, day_name) 

VALUES  

    (1, 'Monday'), 

    (2, 'Tuesday'), 

    (3, 'Wednesday'), 

    (4, 'Thursday'), 

(5, 'Friday'); 

 

ALTER TABLE Schedule 

DROP COLUMN day_of_week, 

ADD day_id INT, 

ADD FOREIGN KEY (day_id) REFERENCES Days(day_id); 

ALTER TABLE Schedule MODIFY schedule_id INT AUTO_INCREMENT;  


The following query will display the value of schedule table instead of id number:
SELECT Schedule.schedule_id, Course.teach_course, Days.day_name, period.time_slot 

FROM Schedule 

INNER JOIN Course ON Schedule.course_id = Course.course_id 

INNER JOIN Days ON Schedule.day_id = Days.day_id 

INNER JOIN period ON Schedule.period_id = Period.period_id; 

 
