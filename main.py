# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os

import requests
import json
import asyncio
from datetime import date, datetime
from time import gmtime, strftime, sleep
import pandas as pd



def getVehicles(name):
    # Use a breakpoint in the code line below to debug your script.
    filename = str(date.today()) + '-TRACCAR.csv'
    # if os.path.isfile('/home/' + os.getlogin() + '/OBA_DATABASE/' + str(date.today()) +'/'+ filename ):
    #     print('Found record: ' + filename)
    # else:
    #     print('No record found: ' + filename)
    #     create_folder(os.makedirs('/home/' + os.getlogin() + '/OBA_DATABASE/' + str(date.today())))
    #     print('Created record: ' + filename)

    traccarrequest = requests.get(
        'http://167.172.12.82:8080/api/v1/key/f78a2e9a/agency/1/command/vehicles?r=%20&format=json')
    response = json.loads(traccarrequest.text)
    response = response["vehicles"]
    fetched = []
    timestamp = str(datetime.now())
    print(response)

    for item in response:
        fetched.append(
            [item['id'], item['vehicleType'], item['loc']['lat'], item['loc']['lon'], item['loc']['time'], timestamp])

    dfTraccar = pd.DataFrame(fetched, columns=['id', 'vehicleType', 'lon', 'lat', 'time', 'timestamp'])
    dfTraccar.to_csv(filename)


def getRoutes(name):
    # Use a breakpoint in the code line below to debug your script.
    filename = str(date.today()) + '-OBA.csv'

    traccarrequest = requests.get('http://167.172.12.82:8080/api/v1/key/f78a2e9a/agency/1/command/gtfs-rt/vehiclePositions?format=human')
    response = traccarrequest.text
    # fetched = []
    data = response[response.find("}"):]
    newdata = data
    for x in range(data.count('entity')):
        newdata = data[data.find('entity')]



    # timestamp = strr(datetime.now())
    #
    # for item in response:
    #     fetched.append(
    #         [item['id'], item['vehicleType'], item['loc']['lat'], item['loc']['lon'], item['loc']['time'], timestamp])
    #
    # dfTraccar = pd.DataFrame(stmod)
    # print(dfTraccar)
    # dfTraccar.to_csv(filename)


def setDir(str):
    print(str)
    os.chdir('/home/' + os.getlogin() + '/OBA_DATABASE/' + str(date.today()))
    pass


if __name__ == '__main__':
    path = os.getcwd(   )

    sec = 15
    for tick in range(0, sec):
        setDir("The current working directory is %s" % path)
        getVehicles('Vehicles ...')
        getRoutes('Routes ...')
        # asyncio.run(runner())
        sleep(1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
