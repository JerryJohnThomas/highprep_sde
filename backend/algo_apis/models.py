from django.db import models

import os

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.username, instance.random_number, ext)
    return os.path.join('media', filename)

# Create your models here.
# models to store the information of the locations of rider that it needs to navigate 
class Rider(models.Model):
    status = models.CharField(max_length=20)
    location_ids = models.JSONField(null=True, blank=True)
    # need to add the bag which will store the ids of inventory items 

# model to store the locations information and geo coordinates 
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    location_name = models.CharField(max_length=150)
   
# making the new model 
class AlgorithmStatusModel(models.Model):
    username = models.EmailField(null=False)
    random_number = models.CharField(max_length=500)
    status = models.CharField(max_length=200)
    # excelSheetName = models.CharField(max_length=1000)
    excelSheetFile = models.FileField(upload_to=content_file_name ,null=True)

