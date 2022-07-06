import os
import requests
import json
import asyncio
from datetime import date, datetime
from time import gmtime, strftime, sleep
import pandas as pd


def getDir():
    savefile = "./OBA_DATABASE/" + str(date.today().strftime("%Y-%m")) + '/'

    if os.path.isdir("./OBA_DATABASE"):
        print('./OBA_DATABASE already exists')
    else:
        os.makedirs("./OBA_DATABASE")
        os.makedirs("./OBA_DATABASE/" + str(date.today().strftime("%Y-%m")) + '/')
        sleep(2)
    return savefile


def getLocs(dir):
    traccarrequest = requests.get(
        'http://167.172.12.82:8080/api/v1/key/f78a2e9a/agency/1/command/vehicles?r=%20&format=json')
    response = json.loads(traccarrequest.text)
    response = response["vehicles"]
    fetched = []
    timestamp = str(datetime.now())

    for item in response:
        fetched.append(
            [item['id'], item['vehicleType'], item['loc']['lat'], item['loc']['lon'], item['loc']['time'], timestamp])

    filedir = os.path.join(dir, str(date.today().strftime("%d")) + '-TRACCAR.csv')
    temp = None
    if os.path.isfile(filedir):
        print(filedir)
        temp = pd.read_csv(filedir)
    dfTraccar = pd.DataFrame(fetched, columns=['id', 'vehicleType', 'lon', 'lat', 'time', 'timestamp'])
    if temp is None:
        dfTraccar.to_csv(filedir)
    else:
        val = pd.concat([temp, dfTraccar])
        val.to_csv(filedir, index=False,
                   columns=['id', 'vehicleType', 'lon', 'lat', 'time', 'timestamp'])


def getRoutes(dir):
    req = requests.get(
        'http://167.172.12.82:8080/api/v1/key/f78a2e9a/agency/1/command/gtfs-rt/vehiclePositions?format=human'
       )
    data = req.text
    data = data.split('\n')

    df = pd.DataFrame()

    prevId = 0

    for x in range(0, len(data)):
        # print(x, data[x])
        length = len(df)

        if 'trip {' in data[x]:
            df.loc[length, 'trip_id'] = data[x + 1]
            df.loc[length, 'start_date'] = data[x + 2]
            df.loc[length, 'route_id'] = data[x + 4]
            df.loc[length, 'lat'] = data[x + 7]
            df.loc[length, 'loc'] = data[x + 8]
            df.loc[length, 'bearing'] = data[x + 9]
            df.loc[length, 'current_stop_sequence'] = data[x + 11]
            df.loc[length, 'current_status'] = data[x + 12]
            df.loc[length, 'timestamp'] = data[x + 13]
            df.loc[length, 'stop_id'] = data[x + 14]
            df.loc[length, 'stop_id'] = data[x + 16]
            x += 15

    temp = None
    filedir = os.path.join(dir, str(date.today().strftime("%d")) + '-TRIPS.csv')

    if os.path.exists(filedir):
        print(filedir)
        temp = pd.read_csv(filedir)
    if temp is None:
        df.to_csv(filedir)
    else:
        temp = pd.concat([temp, df])
        temp.to_csv(filedir, index=False)


def getVehicles(dir):
    req = requests.get(
        'http://167.172.12.82:8080/api/v1/key/f78a2e9a/agency/1/command/gtfs-rt/tripUpdates?format=human')
    data = req.text
    data = data.split('\n')

    df = pd.DataFrame()

    for x in range(0, len(data)):
        # print(x, data[x])
        length = len(df)

        if 'entity {' in data[x]:
            df.loc[length, 'id'] = data[x + 1]
            df.loc[length, 'trip_id'] = data[x + 4]
            df.loc[length, 'start_date'] = data[x + 5]
            df.loc[length, 'route_id'] = data[x + 7]

            x += 7
            stopsInEntity = 0
            notVehicle = True
            while notVehicle:

                if 'vehicle' in data[x]:
                    notVehicle = False
                elif 'stop_time_update' in data[x]:
                    df.loc[length, 'stop_sequence' + str(stopsInEntity)] = data[x + 1]
                    df.loc[length, 'departure_time' + str(stopsInEntity)] = data[x + 3]
                    df.loc[length, 'stop_id' + str(stopsInEntity)] = data[x + 5]
                    x += 5
                    stopsInEntity += 1
                x += 1



    temp = None
    filedir = os.path.join(dir, str(date.today().strftime("%d")) + '-PREDICTIONS.csv')

    if os.path.exists(filedir):
        print(filedir)
        temp = pd.read_csv(filedir)
    if temp is None:
        df.to_csv(filedir)
    else:
        temp = pd.concat([temp, df])
        temp.to_csv(filedir, index=False)


def checkTime():
    if datetime.now().weekday() and 5 <= datetime.now().hour <= 7:
        return True
    else:
        return False


if __name__ == '__main__':

    savefile = getDir()
    isRunning = checkTime()

    while not isRunning:
        getLocs(savefile)
        getRoutes(savefile)
        getVehicles(savefile)

        sleep(1)
