import numpy as np
import pandas as pd
import seaborn as sns
import mysql.connector

def createReport(freq, fName, lName, email):
    if freq == "daily":
        createDailyReport(fName, lName, email)
    elif freq == "weekly":
        createWeeklyReport(fName, lName, email)
    elif freq == "bi-weekly":
        createBiWeeklyReport(fName, lName, email)
    elif freq == "monthly":
        createMonthlyReport(fName, lName, email)
    elif freq == "limit":
        createLimitReport(fName, lName, email)


def createDailyReport(fName, lName, email):
    pass
def createWeeklyReport(fName, lName, email):
    pass
def createBiWeeklyReport(fName, lName, email):
    pass
def createMonthlyReport(fName, lName, email):
    pass
def createLimitReport(fName, lName, email):
    pass
