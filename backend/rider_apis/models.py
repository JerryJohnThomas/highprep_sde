from django.db import models

# Create your models here.

# now defining the model to store the information about each post 
class Bag(models.Model):
    bag_id = models.AutoField(primary_key=True)
    item_list = models.JSONField(default={"item" : []})
    bag_size = models.IntegerField(default=640000)
