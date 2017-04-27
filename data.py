# @Author: Justin Hershberger
# @Date:   27-03-2017
# @Filename: data.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 26-04-2017



from pymongo import MongoClient
from datetime import datetime, timedelta
import requests


#connect to the running instance of the mongo server
client = MongoClient()

# connect to the solar db on mongo
db = client.CS5890_Solar

# this gets today's date and yesterday's so we can get yesterday's data each day
# today = str((datetime.today() - timedelta(2)).date())
# yesterday = str((datetime.today() - timedelta(3)).date())


def usu_climate_api():
    total = 0
    url = "https://climate.usurf.usu.edu/API/api.php/v1/key=TESTKEY/stationSrch/stationId=1266802/getHourly/startDate=" + yesterday + "/endDate="+ today +"/units=english"
    r = requests.get(url)
    jsn = r.json()
    solar = {}

    # this gets the solar radiaion for each day
    for key in jsn:
        if key == 'payload':
            for ky in jsn[key]:
                if 'solarmj' in ky:
                    # print(ky['solar'])
                    solar[ky['date_time']] = ky['solarmj']

    for el in solar:
        day = datetime.strptime(el, '%Y-%m-%d %H:%M:%S')
        print el,solar[el]
        print "Day: ", datetime.strftime(day, '%Y-%m-%d')
        total += float(solar[el])

        #this inserts the solar radiation for the day to mongo
        # result = db.display_solar_post.insert_one(
        #     {
        #             "date": el,
        #             "source": "Utah Climate Center",
        #             "station": "1266802",
        #             "solar_radiation": solar[el]
        #     }
        # )
    print total

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
    url = "http://api.openweathermap.org/data/2.5/forecast?id=5777544&APPID=1966474faa754fc3b6656f04bbeaa2a7"
    r = requests.get(url)
    print r.json()

# this gets solar data
def nrel_api():
    token = 'M8B9A68twIVsCzVfX9OrJ7R6VBwh5fJkIIRMTWrT'

    # need to update to get info for Logan
    url = 'https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key=M8B9A68twIVsCzVfX9OrJ7R6VBwh5fJkIIRMTWrT&lat=41&lon=-111'
    r = requests.get(url)
    print r.json()


def postDay():
    today = str((datetime.today()).date())
    yesterday = str((datetime.today() - timedelta(1)).date())
    postHourly(yesterday=yesterday, today=today)
    # try:
    #     p = db.disp
    # except Post.DoesNotExist: # if the date isn't in the database then add it


def postHourly(yesterday, today):
    fl = open('C:/Users/Justin/Documents/GitHub/CS5890_Final/Hourly_Data/'+ yesterday + '-' + today, 'w')
    fl.write("Hourly Data For: " + yesterday + " to " + today + '\n\n\n')
    url = "https://climate.usurf.usu.edu/API/api.php/v1/key=TESTKEY/stationSrch/stationId=1266802/getHourly/startDate=" + yesterday + "/endDate="+ today +"/units=english"
    r = requests.get(url)
    jsn = r.json()
    solar = {}
    day_hr = []
    day_hr_watt = []
    day_hr_air_temp = []
    solar_watts = {}
    air_temp = {}
    # this gets the solar radiaion for each day
    for key in jsn:
        if key == 'payload':
            for ky in jsn[key]:
                if 'solarmj' in ky:
                    # print(ky['solarmj'])
                    solar[ky['date_time']] = ky['solarmj']

                    for el in solar:
                        # print el,solar[el]
                        day = datetime.strptime(el, '%Y-%m-%d %H:%M:%S')
                        day_hr.append([datetime.strftime(day, '%H:%M'), str(solar[el]), '<br>'])
                        # fl.write("Solar Radiation in Mj/m^2: " + str(datetime.strftime(day, '%H:%M:%S')) + ": " + str(solar[el]) + '\n')
                        #this inserts the solar radiation for the day to mongo
                if 'solar' in ky:
                    solar_watts[ky['date_time']] = ky['solar']

                    for el in solar_watts:
                        # print el,solar[el]
                        day = datetime.strptime(el, '%Y-%m-%d %H:%M:%S')
                        day_hr_watt.append([datetime.strftime(day, '%H:%M:%S'), str(solar_watts[el]), '<br>'])
                        # fl.write("Solar Radiation in W/m^2: " + str(datetime.strftime(day, '%H:%M:%S')) + ": " + str(solar_watts[el]) + '\n')
                if 'airt_avg' in ky:
                    air_temp[ky['date_time']] = ky['airt_avg']

                    for el in air_temp:
                        # print el,solar[el]
                        day = datetime.strptime(el, '%Y-%m-%d %H:%M:%S')
                        day_hr_air_temp.append([datetime.strftime(day, '%H:%M:%S'), str(air_temp[el]), '<br>'])
                        # fl.write('Air Temp Avg: ' + str(datetime.strftime(day, '%H:%M:%S')) + ": " + str(air_temp[el]) + '\n')

    #this gets a sorted version of the hourly breakdowns
    new_day_hr = list()
    new_day_hr_watts = list()
    new_day_hr_air_temp = list()
    map(lambda x: not x in new_day_hr and new_day_hr.append(x), day_hr)
    map(lambda x: not x in new_day_hr_watts and new_day_hr_watts.append(x), day_hr_watt)
    map(lambda x: not x in new_day_hr_air_temp and new_day_hr_air_temp.append(x), day_hr_air_temp)

    new_day_hr_times = []
    new_day_hr_data = []
    fl.write('Solar Radiation in Mj/m^2\n')
    for itm in new_day_hr:
        new_day_hr_times.append(itm[0])
        new_day_hr_data.append(itm[1])
        fl.write(str(itm[0]) + '    ' + str(itm[1]) + '\n')


    fl.write('\n\n')
    fl.write('Air Temperature in Fahrenheit\n')
    for itm in new_day_hr_air_temp:
        fl.write(str(itm[0]) + '    ' + str(itm[1]) + '\n')

    fl.close()


    # result = Post.objects.create(
    #     date_air_temp = new_day_hr_air_temp,
    #     date_hr_mj = new_day_hr,
    #     date_hr_watt = new_day_hr_watts,
    #     date= datetime.strftime(day, '%Y-%m-%d'),
    #     source= "Utah Climate Center",
    #     station= "1266802",
    #     solar_radiation= solar[el]
    # )
    #
    #
    # result.save()



# usu_climate_api()
# noaa_api()
# openweather_api()
# nrel_api()
postDay()
