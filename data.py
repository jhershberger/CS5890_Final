# @Author: Justin Hershberger
# @Date:   27-03-2017
# @Filename: data.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 29-03-2017



import requests

def usu_climate_api():
    url = "https://climate.usurf.usu.edu/API/api.php/v1/key=TESTKEY/stationSrch/stationId=1266802/getDaily/startDate=2016-04-05/endDate=2016-05-28/units=english"
    r = requests.get(url)
    print(r.json())

def noaa_api():
    # this url will get the dataset for the Logan, Ut station
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=GHCND:USC00425186&startdate=2017-01-01&enddate=2017-02-01"
    token = {'token': 'dqZAsslYPbTcxXNqcpHvWiMHOsTcTdSh'}
    r = requests.get(url, headers = token)
    print(r.json())

def openweather_api():
    # this uses the CS5890 token for Logan, UT
    #  I need to update this to get more info, maybe a forecast
    url = "http://api.openweathermap.org/data/2.5/weather?id=5777544&APPID=1966474faa754fc3b6656f04bbeaa2a7"
    r = requests.get(url)
    print(r.json())

# this gets solar data
def nrel_api():
    token = 'M8B9A68twIVsCzVfX9OrJ7R6VBwh5fJkIIRMTWrT'

    # need to update to get info for Logan
    url = 'https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key=M8B9A68twIVsCzVfX9OrJ7R6VBwh5fJkIIRMTWrT&lat=41&lon=-111'
    r = requests.get(url)
    print(r.json())

# usu_climate_api()
# noaa_api()
# openweather_api()
nrel_api()
