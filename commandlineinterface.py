import mysql.connector
import reports
import datetime
from datetime import timedelta
def getValidUsername(cursor):
    try:
        while True:
            username = input("Enter username: ")
            if len(username) >= 1 and len(username) <=20:
                statement = "SELECT username FROM USER WHERE username=%s"
                cursor.execute(statement, [username])
                result = cursor.fetchall()
                if len(result) > 0:
                    print("Username Already Taken\n")
                else: return username
            else: print("Username must be between 1 and 20 characters")
    except Exception as e:
        print("An error occurred.")
        print(e)
    
def getPassword():
    while True:
        password = input("Enter password: ")
        if len(password) >= 1 and len(password) <= 50:
            password2 = input("Re-enter password: ")
            if password2 == password:
                #could add encryption here
                return password
            else:
                print("Passwords were different. Please try again.")
        else: print("Password must be between 1 and 50 characters")

def getName(firstlast):
    while True:
        name = input("Enter {} name: ".format(firstlast))
        if len(name) >=1 and len(name) <= 20:
            return name
        else:
            print("Name must be between 1 and 20 characters")

def getEmail():
    while True:
        email = input("Enter email address: ")
        #could add email regex validation here
        if len(email) >=1 and len(email) < 50:
            return email
        else:
            print("Email must be betweeen 1 and 50 characters")


def addUser():
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    username = getValidUsername(cursor)
    password = getPassword()
    fName = getName("first")
    lName = getName("last")
    email = getEmail()
    statement = "INSERT INTO User VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(statement, [username, password, fName, lName, email])
    dbConnection.commit()
    cursor.close()
    dbConnection.close()
    print("User successfully created")

def validateUser():
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    username = input("Enter username: ")
    password = input("Enter password: ")
    statement = "SELECT username FROM USER WHERE username=%s AND password=%s"
    cursor.execute(statement, [username, password])
    result = cursor.fetchall()
    cursor.close()
    dbConnection.close()
    if len(result) > 0: return username
    else: return ""

def addReportToDB(freq, username):
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = "INSERT INTO Report(freq, user) VALUES (%s, %s)"
    cursor.execute(statement, [freq, username])
    dbConnection.commit()
    cursor.close()
    dbConnection.close()
    print("Successfully scheduled {} report for user {}".format(freq, username))

def addLimitReportToDB(username, limit):
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = "INSERT INTO Report(`freq`, `user`, `limit`) VALUES (%s, %s, %s)"
    cursor.execute(statement, ["limit", username, limit])
    dbConnection.commit()
    cursor.close()
    dbConnection.close()
    print("Successfully scheduled limit report of {}m^3 for user {}".format(limit, username))

def scheduleReport(username):
    while True:
        print("How often would you like your report?")
        print("   1: daily\n   2: weekly\n   3: bi-weekly\n   4: monthly\n   5: upon reaching a limit\n   6: cancel")
        userInput = input("Enter your choice: ")
        if userInput == "1":
            addReportToDB("daily", username)
            break
        elif userInput == "2":
            addReportToDB("weekly", username)
            break
        elif userInput == "3":
            addReportToDB("bi-weekly", username)
            break
        elif userInput == "4":
            addReportToDB("monthly", username)
            break
        elif userInput == "5":
            limit = 0
            while True:
                try:
                    userInput2 = input("Enter your limit in m^3: ")
                    limit = float(userInput2)
                    break
                except ValueError:
                    print("Limit must be a number.")
            addLimitReportToDB(username, limit)
            break
        elif userInput == "6":
            break
        else:
            print("Invalid input.")



def instantReport(freq, username):
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = "SELECT FName, LName, email FROM USER WHERE username=%s"
    cursor.execute(statement, [username])
    result = cursor.fetchall()[0]
    fName = result[0]
    lName = result[1]
    email = result[2]
    cursor.close()
    dbConnection.close()
    reports.createReport(freq, fName, lName, email, currentTime=datetime.datetime.now())

def viewTable():
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = ""
    while True:
        userInput = input("Which table would you like to view? 1: Raw Data, 2: Daily Data, 3: Monthly data, 4: cancel: ")
        if userInput == "1":
            statement = "SELECT * FROM water_Meter_Raw"
            break
        elif userInput == "2":
            statement = "SELECT * FROM day_Meter_Data"
            break
        elif userInput == "3":
            statement = "SELECT * FROM month_Meter_Data"
            break
        elif userInput == "4":
            break
        else:
            print("Invalid input")
    if statement != "":
        cursor.execute(statement)
        results = cursor.fetchall()
        for result in results:
            print(result)
    cursor.close()
    dbConnection.close()
            

if __name__ == '__main__':
    while True:
        username = ""
        while True:
            userInput = input("Enter 1 to log in, or 2 to create a new user: ")
            if userInput == "1":
                username = validateUser()
                if username != "":
                    break
                else: print("Invalid credentials")
            elif userInput == "2":
                addUser()
            else:
                print("Invalid input")
        print("Welcome user.")
        while True:
            userInput = input("Enter 1 to schedule automatic report, 2 to generate an instant daily report, 3 to generate an instant monthly report, 4 to view a database table, or 5 to sign out: ")
            if userInput == "1":
                scheduleReport(username)
            elif userInput == "2":
                instantReport("daily", username)
            elif userInput == "3":
                instantReport("monthly", username)
            elif userInput == "4":
                viewTable()
            elif userInput == "5":
                break
            else:
                print("Invalid input")
    
