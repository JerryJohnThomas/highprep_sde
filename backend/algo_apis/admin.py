from django.contrib import admin
from .models import Rider, Location, AlgorithmStatusModel
# Register your models here.
admin.site.register(Rider);
admin.site.register(Location)
admin.site.register(AlgorithmStatusModel)