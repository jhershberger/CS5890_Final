# @Author: Justin Hershberger
# @Date:   01-04-2017
# @Filename: models.py
# @Last modified by:   Justin Hershberger
# @Last modified time: 01-04-2017



from django.db import models

# Create your models here.
class Post(models.Model):
    source = models.TextField()
    date = models.TextField()
    solar_radiation = models.FloatField()
    station = models.IntegerField()
