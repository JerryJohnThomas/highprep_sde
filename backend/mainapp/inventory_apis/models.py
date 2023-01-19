from django.db import models


# Create your models here.
# models to store the information of the locations of rider that it needs to navigate 
class Item(models.Model):
    item_name = models.CharField(),
    item_volume = models.CharField(),
    
    def __str__(self):
        return self.item_name