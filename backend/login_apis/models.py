from django.db import models


# Create your models here.
# here i will be making the personInfo models for this purpose 
class PersonInfo(models.Model):
    name = models.TextField(max_length=100)
    username = models.TextField(max_length=150)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    age = models.IntegerField()
    person_type = models.CharField(max_length=100)
    bike_details = models.CharField(max_length=200)

    def __str__(self):
        return self.name


