from django.db import models
from login_apis.models import PersonInfo 
import os

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.username, instance.random_number, ext)
    return os.path.join('media', filename)


def content_file_name2(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s.%s" % (instance.username, instance.random_number,"pickup", ext)
    return os.path.join('dynamic_pickup_points', filename)

# Create your models here.
# models to store the information of the locations of rider that it needs to navigate 
# do note that there the username is of the warehouse manager which has launched the start algo and under 
# which this rider comes this acts as the foreign key for this purpose 
class Rider(models.Model):
    username = models.EmailField(null=False, default="pandey7@gmail.com")
    email = models.EmailField(primary_key=True, default="1@gmail.com")
    # warehouse_manager_email = models.EmailField(null=False, default="war1@gmail.com")   
    random_number = models.CharField(max_length=500, default="string")
    status = models.CharField(max_length=20)
    location_ids = models.JSONField(null=True, blank=True)
    bag_id = models.CharField(max_length=100, default="-1")
    
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
    dynamicPickUpExcelSheet = models.FileField(upload_to=content_file_name2, null=True)
    rider_to_location = models.JSONField(default=[]);

# # making the new model to store the results of the algorithm 
# class ResultModel(models.Model):
#     username = models.EmailField(null=False)
#     random_number = models.CharField(max_length=500)
#     rider_to_location = models.JSONField()