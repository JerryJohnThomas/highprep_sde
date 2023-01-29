from django.db import models

# Create your models here.

# now defining the model to store the information about each post 
class Item(models.Model):
    item_name = models.CharField(max_length=250)
    item_volume = models.CharField(max_length=250)
    item_count = models.IntegerField(default=1)
  

    def __str__(self):
        return self.item_name