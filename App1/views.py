from django.shortcuts import render, HttpResponse, redirect
import mysql.connector
import os
from datetime import date


def index(request):
    return render(request, "website.html")


def login(request):
    # Code for getting information from frontend
    cnx = mysql.connector.connect(user='root', password='woshiguapi',
                                  host='127.0.0.1', database='TutorBird')
    cursor = cnx.cursor()

    if request.method == "GET":
        return render(request, "login.html")

    global username
    global user_role

    username = request.POST.get("username")
    password = request.POST.get("password")

    try:
        # Quering for the corresponding password based on entered username
        query = (f"SELECT user_password FROM user WHERE user_username = '{username}'")
        cursor.execute(query)
        correctPassword = cursor.fetchone()

        if correctPassword:
            # Validating input password with the password on file
            # If successful, render next website and return the name of the user
            if str(password) == str(correctPassword[0]):
                print("CORRECT PASSWORD, GREAT JOB")
                cursor.execute(f"SELECT user_firstname, user_role FROM user WHERE user_username= '{username}'")
                data = cursor.fetchall()
                cursor.close()
                cnx.close()

                user_role = data[0][1]

                if (data[0][1] == "Tutor"):
                    return render(request, "tutor_interface.html", {'name': data[0][0]})
                else:
                    return render(request, "user_interface.html", {'name': data[0][0]})
            else:

                # If unsucessful login, render the login website again
                cursor.close()
                cnx.close()
                return render(request, "login.html", {"response": 404})
        else:
            # If username doesn't exist, render the website again
            cursor.close()
            cnx.close()
            return render(request, "login.html", {"response": 404})


    except Exception as e:
        print(repr(e))
        return render(request, "login.html")


def register(request):
    # Code for getting inputs from website
    cnx = mysql.connector.connect(user='root', password='woshiguapi',
                                  host='127.0.0.1', database='TutorBird')
    cursor = cnx.cursor()

    if request.method == "GET":
        return render(request, "register.html")

    username = request.POST.get("username")
    password = request.POST.get("password")
    firstN = request.POST.get("firstN")
    lastN = request.POST.get("lastN")
    email = request.POST.get("email")
    dob = request.POST.get("dob")
    phoneNum = request.POST.get("phoneNum")
    role = request.POST.get("role")

    try:

        # Code for registering new users into the database
        # Also add users to tutor and student database depending on input roles

        if username and password and firstN and lastN and email and dob and phoneNum and role:
            query = (
                f"INSERT INTO user (user_firstname,user_lastname, user_dob, user_email, user_phoneNum, user_username, user_password, user_joinDate, user_role)"
                f"VALUES ('{firstN}', '{lastN}', '{dob}', '{email}', '{phoneNum}', '{username}', '{password}', '{date.today()}', '{role}')")

            cursor.execute(query)
            cnx.commit()
            print("User input successful")

            cursor.execute(f"SELECT user_id FROM user WHERE user_username = '{username}'")
            user_id = cursor.fetchone()
            print(f"The userid is {user_id[0]}")

            if role == "Tutor":
                query = (f"INSERT INTO tutor (user_id)"
                         f"VALUES ('{user_id[0]}')")
                cursor.execute(query)
                print("Tutor successfully added")
                cnx.commit()
                cursor.close()
                cnx.close()
            else:
                query = (f"INSERT INTO student (user_id)"
                         f"VALUES ('{user_id[0]}')")
                cursor.execute(query)
                print("Student successfully added")
                cnx.commit()
                cursor.close()
                cnx.close()

            return render(request, "register.html")

        else:
            return render(request, "register.html", {"response": 404})

    except Exception as e:
        print(repr(e))
        return render(request, "register.html")


def interface(request):

    return render(request, "user_interface.html")


def interfaceTutor(request):
    cnx = mysql.connector.connect(user='root', password='woshiguapi',
                                  host='127.0.0.1', database='TutorBird')
    cursor = cnx.cursor()
    if request.method == "POST":
        # Retrieve the tutor_id using the global username variable
        cursor.execute(f"SELECT user_id FROM user WHERE user_username = '{username}'")
        user_id = cursor.fetchone()[0]
        cursor.execute(f"SELECT tutor_id FROM tutor WHERE user_id= '{user_id}'")
        tutor_id = cursor.fetchone()[0]

        # Assuming that i represents day (0-6, Monday-Sunday) and j represents period (0-4, 1st-5th hour)
        for i in range(0, 7, 1):
            for j in range(0, 5, 1):
                course_name = request.POST.get(f"text{i}{j}")
                # If there is a course selected for this slot, convert the course name to course_id and store it in the database
                if course_name:
                    # Fetch the course_id corresponding to the course_name
                    cursor.execute(f"SELECT course_id FROM course WHERE teach_course = '{course_name}'")
                    course_id = cursor.fetchone()[0]

                    query = (
                        f"INSERT INTO Schedule (tutor_id, course_id, day_id, period_id)"
                        f"VALUES ('{tutor_id}', '{course_id}', '{j + 1}', '{i + 1}')")

                    cursor.execute(query)
                    print(f"Schedule input successful for Day: {i + 1} Period: {j + 1}")

        cnx.commit()  # Make sure to commit changes to the database
    return render(request, "tutor_interface.html")


def findtutors(request):
    cnx = mysql.connector.connect(user='root', password='woshiguapi',
                                  host='127.0.0.1', database='TutorBird')
    cursor = cnx.cursor()

    query = ("SELECT tutor.tutor_id, user.user_firstname FROM tutor "
             "INNER JOIN user ON tutor.user_id=user.user_id")
    cursor.execute(query)
    query = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render(request, "find_tutors.html", {"query": query})


def schedule(request):

    tutor_id = request.POST.get("tutorid")

    cnx = mysql.connector.connect(user='root', password='woshiguapi',
                                  host='127.0.0.1', database='TutorBird')
    cursor = cnx.cursor()

    query = (f'SELECT period_id, day_id, course_id from tutorbird.schedule WHERE tutor_id = {tutor_id}')

    cursor.execute(query)

    period_dict = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}

    schedule_dict = {1: "Biology", 2: "Chinese", 3: "World History", 4: "Mathematics",
                     5: "Government", 6: "Geography", 7: "Literature", 8: "Chemistry", 9: "Physics"}

    guapi = cursor.fetchall()

    print(guapi)
    dict = {}

    for i in range(len(guapi)):
        dict[f"text{period_dict[guapi[i][0]]}{period_dict[int(guapi[i][1])]}"] = schedule_dict[guapi[i][2]]

    return render(request, "view_schedule.html", {'tutor_id': tutor_id, **dict})


def inputSchedule(request):
    cnx = mysql.connector.connect(user='root', password='woshiguapi',
                                  host='127.0.0.1', database='TutorBird')
    cursor = cnx.cursor()

    cursor.execute(
        f"SELECT tutor_id FROM tutor INNER JOIN user ON tutor.user_id = user.user_id WHERE user.user_username = '{username}'")

    tutor_id = cursor.fetchone()

    query = (f'SELECT period_id, day_id, course_id from tutorbird.schedule WHERE tutor_id = {tutor_id[0]}')

    cursor.execute(query)

    period_dict = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}

    schedule_dict = {1: "Biology", 2: "Chinese", 3: "World History", 4: "Mathematics",
                     5: "Government", 6: "Geography", 7: "Literature", 8: "Chemistry", 9: "Physics"}

    guapi = cursor.fetchall()

    print(guapi)
    dict = {}

    for i in range(len(guapi)):
        dict[f"text{period_dict[guapi[i][0]]}{period_dict[int(guapi[i][1])]}"] = schedule_dict[guapi[i][2]]

    return render(request, "tutor_course.html", dict)


def success(request):
    cnx = mysql.connector.connect(user='root', password='woshiguapi',
                                  host='127.0.0.1', database='TutorBird')
    cursor = cnx.cursor()

    form_data = request.POST.get('highlighted-cells')
    print(form_data)
    form_data = form_data.split(",")
    print(form_data)
    row_data = request.POST.get('highlighted-row')
    print(row_data)
    row_data = [int(x) for x in row_data.split(',')]
    print(row_data)
    column_data = request.POST.get('highlighted-column')
    print(column_data)
    column_data = [int(x) for x in column_data.split(',')]
    print(column_data)
    tutor_id = request.POST.get("tutor_id")

    print(f"The user id is {username}, and the role of the user is {user_role}")

    for i in range(len(form_data)):
        print(f'{row_data[i]}{column_data[i]}  {form_data[i]}')

    cursor.execute(f"SELECT user_id FROM user WHERE user_username = '{username}'")
    user_id = cursor.fetchone()[0]
    print(user_id)

    for i in range(len(form_data)):
        query = "INSERT INTO session (subject_id, day_id, period_id, tutor_id, user_id) "
        query += "VALUES (%s, %s, %s, %s, %s)"
        values = (form_data[i], row_data[i] + 1, column_data[i] + 1, tutor_id, user_id)
        cursor.execute(query, values)
        cnx.commit()

    return render(request, "successful.html", {'form_data': form_data})


def help(request):
    return render(request, "help.html")


def aboutme(request):
    if request.method == "GET":
        return render(request, "about_me.html")
    print(request.POST)
    print(request.FILES)
    file_object = request.FILES.get("fileInput")
    fileOpen = open(os.path.join('App1/dynamic', file_object.name), mode='wb')
    for chunk in file_object.chunks():
        fileOpen.write(chunk)
    fileOpen.close()
    return HttpResponse('File uploaded successfully.')

def myschedule(request):
    cnx = mysql.connector.connect(user='root', password='woshiguapi',
                                  host='127.0.0.1', database='TutorBird')
    cursor = cnx.cursor()

    cursor.execute(f"SELECT user_id from user WHERE user_username = '{username}'")

    user_id = cursor.fetchone()[0]

    query = (f"""SELECT 
    Tutor.user_id AS 'Tutor User Id',
    tutor_name.user_firstname AS 'Tutor Name',
    Student.user_id AS 'Student User Id',
    student_name.user_firstname AS 'Student Name',
    Days.day_name AS 'Day of Week',
    Period.time_slot AS 'Time of Day',
    subject_id AS 'Subject'
FROM
    session
        INNER JOIN
    tutor ON session.tutor_id = Tutor.tutor_id 
        INNER JOIN
    user AS tutor_name ON tutor.user_id = tutor_name.user_id
        INNER JOIN
    student ON session.user_id = Student.user_id
        INNER JOIN
    user AS student_name ON student.user_id = student_name.user_id
        INNER JOIN
    days ON session.day_id = Days.day_id
        INNER JOIN
    period ON session.period_id = Period.period_id
WHERE
    Student.user_id = {user_id}
ORDER BY 
    Days.day_id;
""")
    cursor.execute(query)
    guapi = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render(request, 'schedule.html', {'query' : guapi})