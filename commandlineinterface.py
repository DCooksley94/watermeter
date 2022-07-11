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

def scheduleReport(username):
    pass

def instantReport(freq, username):
    pass

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
            userInput = input("Enter 1 to schedule automatic report, 2 to generate an instant daily report, 3 to generate an instant monthly report, or 4 to sign out: ")
            if userInput == "1":
                scheduleReport(username)
            elif userInput == "2":
                instantReport("daily", username)
            elif userInput == "3":
                instantReport("monthly", username)
            elif userInput == "4":
                break
            else:
                print("Invalid input")
    
