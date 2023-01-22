from django.db import models

import os

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.username, instance.random_number, ext)
    return os.path.join('media', filename)

# Create your models here.
# models to store the information of the locations of rider that it needs to navigate 
class Rider(models.Model):
    email = models.EmailField(primary_key=True, default="1@gmail.com")
    status = models.CharField(max_length=20)
    location_ids = models.JSONField(null=True, blank=True)
    # need to add the bag which will store the ids of inventory items 

# model to store the locations information and geo coordinates 
class Location(models.Model):
    username = models.EmailField(null=False)
    random_number = models.CharField(max_length=500)
    location_id = models.AutoField(primary_key=True)
    location_array = models.JSONField(null=True)
    # location_name = models.JSONField(null=True)
   
# making the new model 
class AlgorithmStatusModel(models.Model):
    username = models.EmailField(null=False)
    random_number = models.CharField(max_length=500)
    status = models.CharField(max_length=200)
    # excelSheetName = models.CharField(max_length=1000)
    excelSheetFile = models.FileField(upload_to=content_file_name ,null=True)

