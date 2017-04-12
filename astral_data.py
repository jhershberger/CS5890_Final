# @Author: Justin Hershberger
# @Date:   04-04-2017
# @Filename: astral_data.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 12-04-2017



from datetime import datetime, timedelta
from astral import Astral

#get the date range
today = datetime.today()
yesterday = today - timedelta(1)

# logan's latitude and longitude
lat = 41.7370
lon = -111.8338

a = Astral()

# open a file for the date range
se_file = open('Astral Data/'+ str(yesterday.date()) + '-' + str(today.date()), 'w')
se_file.write("Elevation and Azimuth Data from " + str(yesterday.date()) + " to " + str(today.date()) + "\n\n" )

se_file.write("Solar Noon: " + str(a.solar_noon_utc(date=today,longitude=lon)) + "\n\n")
se_file.write("Solar Midnight: " + str(a.solar_midnight_utc(date=today,longitude=lon)) + "\n\n")

# there are 1440 minutes in a day
for i in range(1440):
    azimuth = a.solar_azimuth(dateandtime=(today - timedelta(0,0,0,0,i)), latitude=lat, longitude=lon)
    se = a.solar_elevation(dateandtime=(today - timedelta(0,0,0,0,i)), latitude=lat, longitude=lon)
    se_file.write("########################################################\n")
    se_file.write(str(today - timedelta(0,0,0,0,i)) + "- elevation: " + str(se) + "\n")
    se_file.write(str(today - timedelta(0,0,0,0,i)) + "- azimuth: " + str(azimuth) + "\n")
    se_file.write("########################################################\n\n")

se_file.close()
