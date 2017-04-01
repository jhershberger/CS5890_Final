# @Author: Justin Hershberger
# @Date:   01-04-2017
# @Filename: urls.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 01-04-2017


from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name="index"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
