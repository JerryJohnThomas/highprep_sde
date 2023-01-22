from django.contrib import admin
from .models import Rider, Location, AlgorithmStatusModel
# Register your models here.

class LocationAdmin(admin.ModelAdmin):
    readonly_fields = ("location_id",)


admin.site.register(Rider);
admin.site.register(Location, LocationAdmin)
admin.site.register(AlgorithmStatusModel)