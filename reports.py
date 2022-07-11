from email.message import EmailMessage
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import datetime
from datetime import timedelta
import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import base64
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path

SCOPES = ['https://www.googleapis.com/auth/gmail.addons.current.action.compose', 'https://mail.google.com/']


email_username="rfutilitytracker@gmail.com"

def createReport(freq, fName, lName, email, currentTime):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    subject = "Your Water Usage Report"
    body = ""
    if freq == "limit":
        body = "Hello {0} {1}, \n\n This email is notifying you that you have reached your chosen monthly limit as of {2}. Attached is your water usage report. \n\n\n Thank you for choosing Rod & Friends".format(fName, lName, currentTime.strftime("%x"))
    else:
        body = "Hello {0} {1}, \n\n Attached is your {2} water usage report for {3}. \n\n\n Thank you for choosing Rod & Friends".format(fName, lName, freq, (currentTime - timedelta(days=1)).strftime("%x"))
    receiver_email = email

    message = EmailMessage()
    message["From"] = email_username
    message["To"] = receiver_email
    message["Subject"] = subject
    message.set_content(body)
    
    if freq == "daily":
        createDailyReport(currentTime)
    elif freq == "weekly":
        createWeeklyReport(currentTime)
    elif freq == "bi-weekly":
        createBiWeeklyReport(currentTime)
    elif freq == "monthly":
        createMonthlyReport(currentTime)
    elif freq == "limit":
        createLimitReport(currentTime)

    attachment1_filename = 'report.csv'
    type_subtype, _ = mimetypes.guess_type(attachment1_filename)
    maintype, subtype = type_subtype.split('/')
    with open(attachment1_filename, 'rb') as fp:
        attachment_data = fp.read()
    message.add_attachment(attachment_data, maintype, subtype)

    attachment2_filename = 'report.png'
    type_subtype, _ = mimetypes.guess_type(attachment2_filename)
    maintype, subtype = type_subtype.split('/')
    with open(attachment2_filename, 'rb') as fp:
        attachment_data = fp.read()
    message.add_attachment(attachment_data, maintype, subtype)

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }
    service.users().messages().send(userId="me", body=create_message).execute()
    if (os.path.exists("report.csv")):
        os.remove("report.csv")
    if (os.path.exists("report.png")):
        os.remove("report.png")


def createDailyReport(currentTime):
    reportDay = (currentTime - timedelta(days=1)).day
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = "SELECT recordDate, volume FROM water_Meter_Raw WHERE DAY(recordDate) = %s"
    cursor.execute(statement, [reportDay])
    result = cursor.fetchall()
    df = pd.DataFrame(data=result, columns=["time", "volume"])
    df=df.set_index('time')
    plt.figure(figsize=(10,8))
    ax = sns.lineplot(x=df.index, y=df["volume"])
    plt.xticks(rotation=45)
    plt.ylabel("Volume (m^3)")
    plt.title("Water report for {}".format((currentTime - timedelta(days=1)).strftime("%x")))
    plt.savefig("report.png")
    df.to_csv("report.csv")
    cursor.close()
    dbConnection.close()


def createWeeklyReport(currentTime):
    reportStartTime = (currentTime - timedelta(days=7))
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = "SELECT recordDate, volume FROM day_Meter_Data WHERE recordDate >= %s AND recordDate < %s"
    cursor.execute(statement, [reportStartTime.strftime('%Y-%m-%d %H:%M:%S'), currentTime.strftime('%Y-%m-%d %H:%M:%S')])
    result = cursor.fetchall()
    df = pd.DataFrame(data=result, columns=["time", "volume"])
    df=df.set_index('time')
    plt.figure(figsize=(10,8))
    ax = sns.lineplot(x=df.index, y=df["volume"])
    plt.xticks(rotation=45)
    plt.ylabel("Volume (m^3)")
    plt.title("Water report for {}".format((currentTime - timedelta(days=1)).strftime("%x")))
    plt.savefig("report.png")
    df.to_csv("report.csv")
    cursor.close()
    dbConnection.close()


def createBiWeeklyReport(currentTime):
    reportStartTime = (currentTime - timedelta(days=14))
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = "SELECT recordDate, volume FROM day_Meter_Data WHERE recordDate >= %s AND recordDate < %s"
    cursor.execute(statement, [reportStartTime.strftime('%Y-%m-%d %H:%M:%S'), currentTime.strftime('%Y-%m-%d %H:%M:%S')])
    result = cursor.fetchall()
    df = pd.DataFrame(data=result, columns=["time", "volume"])
    df=df.set_index('time')
    plt.figure(figsize=(10,8))
    ax = sns.lineplot(x=df.index, y=df["volume"])
    plt.xticks(rotation=45)
    plt.ylabel("Volume (m^3)")
    plt.title("Water report for {}".format((currentTime - timedelta(days=1)).strftime("%x")))
    plt.savefig("report.png")
    df.to_csv("report.csv")
    cursor.close()
    dbConnection.close()


def createMonthlyReport(currentTime):
    reportMonth = (currentTime - timedelta(days=1)).month
    reportYear = (currentTime - timedelta(days=1)).year
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = "SELECT recordDate, volume FROM day_Meter_Data WHERE MONTH(recordDate) = %s AND YEAR(recordDate) = %s"
    cursor.execute(statement, [reportMonth, reportYear])
    result = cursor.fetchall()
    df = pd.DataFrame(data=result, columns=["time", "volume"])
    df=df.set_index('time')
    plt.figure(figsize=(10,8))
    ax = sns.lineplot(x=df.index, y=df["volume"])
    plt.xticks(rotation=45)
    plt.ylabel("Volume (m^3)")
    plt.title("Water report for {}".format((currentTime - timedelta(days=1)).strftime("%x")))
    plt.savefig("report.png")
    df.to_csv("report.csv")
    cursor.close()
    dbConnection.close()


def createLimitReport(currentTime):
    createMonthlyReport(currentTime + timedelta(days=1))

if __name__ == '__main__':
    #currentTime = datetime.datetime(2023, 7, 14)
    #createLimitReport(currentTime)
    pass