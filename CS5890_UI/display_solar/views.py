# @Author: Justin Hershberger
# @Date:   01-04-2017
# @Filename: views.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 01-04-2017



from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template, loader
from models import Post
# Create your views here.

def index(request):
    solar_data = Post.objects.order_by('date')
    template = loader.get_template('display_solar/index.html')
    context = Context({ "solar_data" : solar_data, })
    return HttpResponse(template.render(context))
