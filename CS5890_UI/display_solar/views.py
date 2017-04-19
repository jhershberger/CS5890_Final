# @Author: Justin Hershberger
# @Date:   01-04-2017
# @Filename: views.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 14-04-2017



from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, loader
from models import Post
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
import requests

# Create your views here.

def index(request):
    solar_data = Post.objects.order_by('-date')
    template = loader.get_template('display_solar/index.html')
    context = Context({ "solar_data" : solar_data, })
    return HttpResponse(template.render(context))

def data(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        # posts = Post.objects.get(date=post.date)
    except Post.DoesNotExist:
        raise Http404("The post doesn't exist")

    avg_panel_area = 1.6354806 # m^2
    default_loss_ratio = 0.75
    panel_yield = 250 / avg_panel_area
    daily_sr = post.solar_radiation * 0.01157  # kW / m^2
    energy = avg_panel_area * panel_yield * daily_sr * default_loss_ratio # kWh
    return render(request, 'display_solar/data.html', { 'post': post, 'energy': energy, })

@csrf_exempt
def postDay(request):
    today = str((datetime.today()).date())
    yesterday = str((datetime.today() - timedelta(1)).date())
    try:
        p = Post.objects.get(date=yesterday + ' 23:59:59')
    except Post.DoesNotExist: # if the date isn't in the database then add it
        postHourly(yesterday=yesterday, today=today)
        return HttpResponseRedirect('/display_solar')

    else:
        postHourly(yesterday=yesterday, today=today)
        return HttpResponseRedirect('/display_solar')


def postHourly(yesterday, today):
    url = "https://climate.usurf.usu.edu/API/api.php/v1/key=TESTKEY/stationSrch/stationId=1266802/getHourly/startDate=" + yesterday + "/endDate="+ today +"/units=english"
    r = requests.get(url)
    jsn = r.json()
    solar = {}
    day_hr = []
    day_hr_watt = []
    solar_watts = {}
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
                        day_hr.append([datetime.strftime(day, '%H:%M:%S'), str(solar[el]) + '<br>'])
                        #this inserts the solar radiation for the day to mongo
                if 'solar' in ky:
                    solar_watts[ky['date_time']] = ky['solar']

                    for el in solar_watts:
                        # print el,solar[el]
                        day = datetime.strptime(el, '%Y-%m-%d %H:%M:%S')
                        day_hr_watt.append([datetime.strftime(day, '%H:%M:%S'), str(solar_watts[el]) + '<br>'])

    #this gets a sorted version of the hourly breakdowns
    new_day_hr = list()
    new_day_hr_watts = list()
    map(lambda x: not x in new_day_hr and new_day_hr.append(x), day_hr)
    map(lambda x: not x in new_day_hr_watts and new_day_hr_watts.append(x), day_hr_watt)

    result = Post.objects.create(
        date_hr_mj = new_day_hr,
        date_hr_watt = new_day_hr_watts,
        date= datetime.strftime(day, '%Y-%m-%d'),
        source= "Utah Climate Center",
        station= "1266802",
        solar_radiation= solar[el]
    )
    result.save()
