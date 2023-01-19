from django.db import models

# # Create your models here.
class PersonalInfo(models.Model):
    name = models.TextField(max_length=100),
    username = models.CharField(max_length=100),
    phone_number = models.CharField(max_length=12),
    age = models.IntegerField(),
    person_type = models.TextField(),
    bike_details = models.TextField()
    #     "name" : "rupesh kumar",
        # "username" : "rupeshkumar",
        # "password" : "123",
        # "age" : 21,
        # "phone_number" : "1234567890",
        # "person_type" : "customer",
        # "bike_details" : "some bike details"

    def __str__(self):
        return self.name

