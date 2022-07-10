import time, sys
#import RPi.GPIO as GPIO
import mysql.connector
import datetime
import random
from datetime import timedelta

def createTestingData(startTime, num, interval):
    for i in range(num):
        randomNumbers = random.randrange(0,80000)
        flow = (randomNumbers / 7.5)
        flowLps = (flow / 60) # Converts flow rate to L/sec
        flowm3 = (flowLps / 1000) # Converts flow L/sec to cubic meters
        timeNow = startTime + timedelta(seconds=i*interval)
        currentDate = timeNow.strftime('%Y-%m-%d %H:%M:%S')
        flow_data = { 'date': currentDate, 'flow': flowm3}
        rawDataInsert(flow_data)
        print("inserted flow data: " + str(flow_data))
    

def compileDay(day):
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement1 = "SELECT SUM(volume), recordDate FROM water_Meter_Raw WHERE DAY(recordDate) = %s"
    cursor.execute(statement1, [day])
    result = cursor.fetchall()[0]
    if result[0] is not None:
        day_volume = result[0]
        day_date = result[1].strftime('%Y-%m-%d %H:%M:%S')
        statement2 = "INSERT INTO day_Meter_Data (volume, recordDate) VALUES (%s, %s)"
        cursor.execute(statement2, (day_volume, day_date))
    dbConnection.commit()
    cursor.close()
    dbConnection.close()

def removeDayFromRaw(day):
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = "DELETE FROM water_Meter_Raw WHERE DAY(recordDate) = %s"
    cursor.execute(statement, [day])
    dbConnection.commit()
    print(cursor.rowcount, " record(s) deleted")
    cursor.close()
    dbConnection.close()

def compileMonth(month):
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement1 = "SELECT SUM(volume), recordDate FROM day_Meter_Data WHERE Month(recordDate) = %s"
    cursor.execute(statement1, [month])
    result = cursor.fetchall()[0]
    if result[0] is not None:
        month_volume = result[0]
        month_date = result[1].strftime('%Y-%m-%d %H:%M:%S')
        statement2 = "INSERT INTO month_Meter_Data (volume, recordDate) VALUES (%s, %s)"
        cursor.execute(statement2, (month_volume, month_date))
    dbConnection.commit()
    cursor.close()
    dbConnection.close()

def removeMonthFromDay(month):
    if month == 0: 
        month = 12
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement = "DELETE FROM day_Meter_Data WHERE MONTH(recordDate) = %s"
    cursor.execute(statement, [month])
    dbConnection.commit()
    print(cursor.rowcount, " record(s) deleted")
    cursor.close()
    dbConnection.close()

def getMonthToDate(month):
    dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')
    cursor = dbConnection.cursor()
    statement1 = "SELECT SUM(volume), recordDate FROM day_Meter_Data WHERE Month(recordDate) = %s"
    cursor.execute(statement1, [month])
    volume = cursor.fetchall()[0][0]
    cursor.close()
    dbConnection.close()
    return volume


def rawDataInsert(rawData):
	dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')

	cursor = dbConnection.cursor()

	insert_flow_data = ("Insert into water_Meter_Raw (recordDate, volume) Values (%(date)s, %(flow)s);")

	cursor.execute(insert_flow_data, rawData)

	dbConnection.commit()

	cursor.close()

	dbConnection.close()



def collectData():
    currentTime = datetime.datetime(2022, 6, 30) # ----> This would be now for non-testing purposes
    currentDay = currentTime.day
    currentMonth = currentTime.month
    weekCount = 0
    while True:
        createTestingData(currentTime,144,600) # create one day of data------>The sensor would be running and adding data to the database in its own process (NOT HERE)
        currentTime += timedelta(days=1) # jump time forward --->Have a waiting delay so the loop doesn't run excessively, and update currentTime to now
        if currentTime.day != currentDay: # if it's a new day
            compileDay(currentDay) # compile previous day
            removeDayFromRaw(currentDay) # clear that day's data
            #SEND DAILY REPORTS
            #CHECK DAY OF WEEK AND SEND WEEKLY REPORTS, INCREMENT WEEKCOUNT, SEND BIWEEKLY REPORTS
            #CHECK LIMITS AND SEND LIMIT REPORTS
            currentDay = currentTime.day # update marker day
        if currentTime.month != currentMonth: # if it's a new month
            compileMonth(currentMonth) # compile previous month
            removeMonthFromDay(currentMonth-1) # clear two months ago's data
            #SEND MONTHLY REPORTS
            currentMonth = currentTime.month # update marker month


# This code makes the code only run if this file is ran directly, and not imported from elsewhere.
if __name__ == '__main__':
    collectData()


        

