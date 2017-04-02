# @Author: Justin Hershberger
# @Date:   01-04-2017
# @Filename: urls.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 02-04-2017


from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="display_solar"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<post_id>[a-zA-Z0-9]+$)', views.data, name="data"),
    url(r'^/post/$', views.post, name="post")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
