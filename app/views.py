from flask import render_template
from app import app

import sqlite3, json, re, os

@app.route('/')
def index():
    get_table_names = nav_bar()
    return render_template('index.html',
                           title='Homepage',
                           table_names = get_table_names
                           )

@app.route('/<month>/')
def month(month):
    get_table_names = nav_bar()
    title = month + ' - Homepage'
    dates, requests = daysPerMonth('access_' + month)

    return render_template('month.html',
                           table_names = get_table_names,
                           dates = dates,
                           requests = requests,
                           title = title)

@app.route('/<month>/HttpCode')
def httpCode(month):
    get_table_names = nav_bar()
    returnCodeCount, httpTimeStamp, HTTP200, HTTP201, HTTP202, HTTP302, HTTP304, HTTP400, HTTP401, HTTP403, HTTP404, HTTP405, HTTP406, HTTP500, HTTP502, HTTP503, HTTP504 = returnCodes('access_' + month)
    title = month + ' - HTTP Status Codes'

    return render_template('HttpCode.html',
                           table_names = get_table_names,
                           title = title,
                           returnCodeCount = returnCodeCount,
                           httpTimeStamp = httpTimeStamp,
                           HTTP200 = HTTP200,
                           HTTP201 = HTTP201,
                           HTTP202 = HTTP202,
                           HTTP302 = HTTP302,
                           HTTP304 = HTTP304,
                           HTTP400 = HTTP400,
                           HTTP401 = HTTP401,
                           HTTP403 = HTTP403,
                           HTTP404 = HTTP404,
                           HTTP405 = HTTP405,
                           HTTP406 = HTTP406,
                           HTTP500 = HTTP500,
                           HTTP502 = HTTP502,
                           HTTP503 = HTTP503,
                           HTTP504 = HTTP504
                           )

@app.route('/<month>/LoadProfile')
def loadProfile(month):
    get_table_names = nav_bar()
    timestamps, concurrency = loadProfile('access_' + month)
    title = month + ' - Load Profile'
    date = getDates('access_' + month)

    return render_template('LoadProfile.html',
                           table_names = get_table_names,
                           title = title,
                           timestamps = timestamps,
                           concurrency = concurrency,
                           date = date
                           )

@app.route('/<month>/IPAddress')
def ipAddress(month):
    get_table_names = nav_bar()
    title = month + ' - IP Address'
    uniqueIP, ipAddressTotal = countIPAddresses('access_' + month)

    return render_template('ipAddress.html',
                           table_names = get_table_names,
                           title = title,
                           uniqueIP = uniqueIP,
                           ipAddressTotal = ipAddressTotal
    #                       accessIP = accessIP
                           )

@app.route('/<month>/UserJourneys')
def userJourneys(month):
    get_table_names = nav_bar()
    title = month + ' - User Journeys'

    return render_template('userJourneys.html',
                           table_names = get_table_names,
                           title = title
                           )

@app.route('/<month>/UserAgents')
def userAgents(month):
    get_table_names = nav_bar()
    title = month + ' - User Agents'
    userAgents, userAgentsVals = countUserAgent('access_' + month)

    return render_template('userAgents.html',
                           table_names = get_table_names,
                           title = title,
                           userAgents = userAgents,
                           userAgentsVals = userAgentsVals
                           )

#All Functions for SQL Queries here
def nav_bar():
    connection = sqlite3.connect('C:\\SQLite\\Databases\\testPython.db')
    cursor = connection.cursor()

    cursor.execute('SELECT NAME FROM sqlite_master WHERE TYPE = \'table\';')
    table_names = json.dumps(cursor.fetchall()).replace("\"], [\"", " ").replace("[[\"","").replace("\"]]","").replace("access_","").split()
    connection.close()

    return table_names

def userJourneys(tableName):
    connection = sqlite3.connect('C:\\SQLite\\Databases\\testPython.db')
    cursor = connection.cursor()

    cursor.execute('SELECT DISTINCT IPAddress FROM ' +  tableName+ ';')
    ipAddresses = json.dumps(cursor.fetchall()).replace("\"], [\"", " ").replace("[[\"","").replace("\"]]","").split()

    ipList = []

    for IP in ipAddresses:
        cursor.execute('SELECT IPAddress, Datestamp, Timestamp, URL FROM ' +  tableName + ' WHERE IPAddress=?;', (IP,))
        ipList.append(json.dumps(cursor.fetchall()))

    connection.close()

    return ipList

def returnCodes(tableName):
    #Add more return codes here if necessary
    retCodes = ['200','201','202','302','304','400','401','403','404','405','406','500','502','503','504']

    connection = sqlite3.connect('C:\\SQLite\\Databases\\testPython.db')
    cursor = connection.cursor()

    returnCodes, dateStamps = [], []
    HTTP200, HTTP201, HTTP202, HTTP302, HTTP304, HTTP400, HTTP401, HTTP403, HTTP404, HTTP405, HTTP406, HTTP500, HTTP502, HTTP503, HTTP504 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    cursor.execute('SELECT DISTINCT Timestamp FROM ' + tableName + ';')
    dateStamps = json.dumps(cursor.fetchall()).replace('[["','').replace('"]]','').split('"], ["')

    for time in dateStamps:
        for code in retCodes:
            cursor.execute("SELECT COUNT (HTTPCode) FROM " + tableName + " WHERE Timestamp=? AND HTTPCode=?;", (time, code,))
            if code == '200':
                HTTP200.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '201':
                HTTP201.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '202':
                HTTP202.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '302':
                HTTP302.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '304':
                HTTP304.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '400':
                HTTP400.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '401':
                HTTP401.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '403':
                HTTP403.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '404':
                HTTP404.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '405':
                HTTP405.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '406':
                HTTP406.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '500':
                HTTP500.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '502':
                HTTP502.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '503':
                HTTP503.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

            elif code == '504':
                HTTP504.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

    connection.close()

    return returnCodes, dateStamps, HTTP200, HTTP201, HTTP202, HTTP302, HTTP304, HTTP400, HTTP401, HTTP403, HTTP404, HTTP405, HTTP406, HTTP500, HTTP502, HTTP503, HTTP504

def countUserAgent(tableName):

    connection = sqlite3.connect('C:\\SQLite\\Databases\\testPython.db')
    cursor = connection.cursor()

    cursor.execute('SELECT DISTINCT UserAgent FROM ' + tableName + ';')
    userAgent = json.dumps(cursor.fetchall()).split("], [")
    userAgentLength = len(userAgent)
    x=0

    for agent in userAgent:
        x+=1
        if x==1:
            userAgent[x-1] = userAgent[x-1].replace("[[\"","").replace("\"","")

        elif x==userAgentLength:
            userAgent[x-1] = userAgent[x-1].replace("\"","").replace("]]","")

        else:
            userAgent[x-1] = userAgent[x-1].replace("\"","")

    userAgentVals = []

    for agent in userAgent:
        cursor.execute('SELECT COUNT(UserAgent) FROM ' + tableName + ' WHERE UserAgent=?;', (agent,))
        userAgentVals.append(json.dumps(cursor.fetchall()).replace("[[","").replace("]]",""))

    connection.close()

    return userAgent, userAgentVals

def countIPAddresses(tableName):
    connection = sqlite3.connect('C:\\SQLite\\Databases\\testPython.db')
    cursor = connection.cursor()

    cursor.execute('SELECT DISTINCT IPAddress FROM ' +  tableName+ ';')
    uniqueIP = json.dumps(cursor.fetchall()).replace("\"], [\"", " ").replace("[[\"","").replace("\"]]","").split()

    cursor.execute('SELECT COUNT (DISTINCT IPAddress) FROM ' + tableName + ';')
    countUniqueIP = json.dumps(cursor.fetchall()).replace("[[","").replace("]]","").split()

#    cursor.execute('SELECT COUNT (IPAddress) FROM ' +  tableName + ' WHERE IPAddress=?;', (uniqueIP,))
#    accessIP = json.dumps(cursor.fetchall()).replace("\"], [\"", " ").replace("[[\"","").replace("\"]]","").split()

    connection.close()

    return uniqueIP, countUniqueIP

def daysPerMonth(tableName):
    connection = sqlite3.connect('C:\\SQLite\\Databases\\testPython.db')
    cursor = connection.cursor()
    test = []

    cursor.execute('SELECT DISTINCT Datestamp FROM ' + tableName + ';')
    dateStamps = json.dumps(cursor.fetchall()).replace("\"], [\"", " ").replace("[[\"","").replace("\"]]","").split()

    for date in dateStamps:
        cursor.execute('SELECT COUNT(IPAddress) FROM ' + tableName + ' WHERE Datestamp=?;', (date,))
        test.append(json.dumps(cursor.fetchall()).replace('[[','').replace(']]',''))

    connection.close()

    return dateStamps, test

def getDates(tableName):
    connection = sqlite3.connect('C:\\SQLite\\Databases\\testPython.db')
    cursor = connection.cursor()

    cursor.execute('SELECT DISTINCT Datestamp FROM ' + tableName + ';')
    date = json.dumps(cursor.fetchall()).replace('[["','').replace('"]]','').split('"], ["')

    connection.close()

    return date

def loadProfile(tableName):
    connection = sqlite3.connect('C:\\SQLite\\Databases\\testPython.db')
    cursor = connection.cursor()
    concurrentUsers= []

    cursor.execute('SELECT DISTINCT Timestamp FROM ' + tableName + ';')
    dateStamps = json.dumps(cursor.fetchall()).replace('[["','').replace('"]]','').split('"], ["')

    for time in dateStamps:
        cursor.execute("SELECT COUNT (DISTINCT IPAddress) FROM " + tableName + " WHERE Timestamp=?;", (time,))
        concurrentUsers.append(json.dumps(cursor.fetchall()).replace('[','').replace(']','').replace('\'',''))

    connection.close()

    return dateStamps, concurrentUsers
