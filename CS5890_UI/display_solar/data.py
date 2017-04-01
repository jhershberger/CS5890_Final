# @Author: Justin Hershberger
# @Date:   27-03-2017
# @Filename: data.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 01-04-2017



from pymongo import MongoClient
from datetime import datetime, timedelta
import requests


#connect to the running instance of the mongo server
client = MongoClient()

# connect to the solar db on mongo
db = client.CS5890_Solar

# this gets today's date and yesterday's so we can get yesterday's data each day
today = str(datetime.today().date())
yesterday = str((datetime.today() - timedelta(1)).date())

def usu_climate_api():
    url = "https://climate.usurf.usu.edu/API/api.php/v1/key=TESTKEY/stationSrch/stationId=1266802/getDaily/startDate=" + yesterday + "/endDate="+ today +"/units=english"
    r = requests.get(url)
    jsn = r.json()
    solar = {}

    # this gets the solar radiaion for each day
    for key in jsn:
        if key == 'payload':
            for ky in jsn[key]:
                if 'solarmj' in ky:
                    # print(ky['solarmj'])
                    solar[ky['date_time']] = ky['solarmj']

    for el in solar:
        print el,solar[el]

        #this inserts the solar radiation for the day to mongo
        result = db.daily_solar.insert_one(
            {
                el: {
                    "Source": "Utah Climate Center",
                    "StationID": "1266802",
                    "Solar Radiation": solar[el]
                }
            }
        )

def noaa_api():
    # this url will get the dataset for the Logan, Ut station
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=GHCND:USC00425186&startdate=2017-01-01&enddate=2017-02-01"
    token = {'token': 'dqZAsslYPbTcxXNqcpHvWiMHOsTcTdSh'}
    r = requests.get(url, headers = token)
    # print(r.json())
    jsn = r.json()

    for key in jsn:
        if key == 'results':
            for ky in jsn['results']:
                print ky

def openweather_api():
    # this uses the CS5890 token for Logan, UT
    #  I need to update this to get more info, maybe a forecast
    url = "http://api.openweathermap.org/data/2.5/weather?id=5777544&APPID=1966474faa754fc3b6656f04bbeaa2a7"
    r = requests.get(url)
    print r.json()

# this gets solar data
def nrel_api():
    token = 'M8B9A68twIVsCzVfX9OrJ7R6VBwh5fJkIIRMTWrT'

    # need to update to get info for Logan
    url = 'https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key=M8B9A68twIVsCzVfX9OrJ7R6VBwh5fJkIIRMTWrT&lat=41&lon=-111'
    r = requests.get(url)
    print r.json()


# usu_climate_api()
noaa_api()
# openweather_api()
# nrel_api()
