import time, sys
#import RPi.GPIO as GPIO
import mysql.connector
import datetime
import random
from datetime import timedelta



def rawDataInsert(rawData):
	dbConnection = mysql.connector.connect(user='capstone', password='password', host='127.0.0.1', database='capstoneHugh')

	cursor = dbConnection.cursor()

	insert_flow_data = ("Insert into water_Meter_Raw (recordDate, volume) Values (%(date)s, %(flow)s);")

	cursor.execute(insert_flow_data, rawData)

	dbConnection.commit()

	cursor.close()

	dbConnection.close()

FLOW_SENSOR_GPIO = 13
#Sets a value of 13 to FLOW_SENSOR_GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0
#Sets a value of 0 to count

def countPulse(channel):
   global count
   if start_counter == 1:
      count = count+1
 
#GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)

while True:
    try:
        randomNumbers = random.randrange(0,80000)
        start_counter = 1
        time.sleep(0.5)
        start_counter = 0
        flow = (randomNumbers / 7.5) # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min. flow = (count / 7.5)
        if flow > 0:
            flowLps = (flow / 60) # Converts flow rate to L/sec
            flowm3 = (flowLps / 1000) # Converts flow L/sec to cubic meters
            timeNow = datetime.datetime.now(datetime.timezone(-timedelta(hours=6)))
            currentDate = timeNow.strftime('%Y-%m-%d %H:%M:%S')
            flow_data = { 'date': currentDate, 'flow': flowm3}
            rawDataInsert(flow_data)

        count = 0
        time.sleep(0.5)

    except Exception as e:
        print(e)
        
    except KeyboardInterrupt:
        print('\nkeyboard interrupt!')
        #GPIO.cleanup()
        sys.exit()
