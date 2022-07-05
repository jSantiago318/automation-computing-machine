import os
import requests
import json
import asyncio
from datetime import date, datetime
from time import gmtime, strftime, sleep
import pandas as pd


def getDir():
    savefile = "./OBA_DATABASE/" + str(date.today().strftime("%Y-%m")) + '/' + str(date.today().strftime("%d"))

    if os.path.isdir("./OBA_DATABASE"):
        print('./OBA_DATABASE already exists')
    else:
        os.makedirs("./OBA_DATABASE")
        os.makedirs("./OBA_DATABASE/" + str(date.today().strftime("%Y-%m")))
        os.makedirs("./OBA_DATABASE/" + str(date.today().strftime("%Y-%m")) + '/' + str(date.today().strftime("%d")))
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
        'http://167.172.12.82:8080/api/v1/key/f78a2e9a/agency/1/command/gtfs-rt/tripUpdates?format=human')
    data = str(req.content)
    data = data.split('\\n')



def getVehicles(dir):
    req = requests.get(
        'http://167.172.12.82:8080/api/v1/key/f78a2e9a/agency/1/command/gtfs-rt/vehiclePositions?format=human')
    data = req.text
    data = data.split('\n')

    keywords = ['id', 'latitude', 'longitude']

    df = pd.DataFrame()

    for x in range(0, len(data)):
        print(data[x])
        for word in keywords:
            if word in data[x]:
                df[word].append(data[x].split(':')[1])
    print(df)

if __name__ == '__main__':

    sec = 20
    savefile = getDir()

    for tick in range(0, sec):
        getLocs(savefile)
        getRoutes(savefile)
        getVehicles(savefile)

        sleep(1)
