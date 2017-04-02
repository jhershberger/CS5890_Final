# @Author: Justin Hershberger
# @Date:   01-04-2017
# @Filename: views.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 02-04-2017



from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, loader
from models import Post
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
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
    except Post.DoesNotExist:
        raise Http404("The post doesn't exist")
    avg_panel_area = 1.6354806 # m^2
    default_loss_ratio = 0.75
    panel_yield = 250 / avg_panel_area
    daily_sr = post.solar_radiation * 0.01157  # kW / m^2
    energy = avg_panel_area * panel_yield * daily_sr * default_loss_ratio # kWh
    return render(request, 'display_solar/data.html', { 'post': post, 'energy': energy })

@csrf_exempt
def post(request):
    today = str(datetime.today().date())
    yesterday = str((datetime.today() - timedelta(1)).date())
    try:
        p = Post.objects.get(date=yesterday + ' 23:59:59')
    except Post.DoesNotExist: # if the date isn't in the database then add it

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
                            # print el,solar[el]

                            #this inserts the solar radiation for the day to mongo
                            result = Post.objects.create(
                                date= el,
                                source= "Utah Climate Center",
                                station= "1266802",
                                solar_radiation= solar[el]
                            )
                            result.save()
        return HttpResponseRedirect('/display_solar')

    else:
        return HttpResponseRedirect('/display_solar')
