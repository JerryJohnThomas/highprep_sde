from django.db import models


# Create your models here.
# models to store the information of the locations of rider that it needs to navigate 
class Rider(models.Model):
    status = models.CharField(max_length=20)
    location_ids = models.JSONField(null=True, blank=True)


# model to store the locations information and geo coordinates 
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    location_name = models.CharField(max_length=150)
    
