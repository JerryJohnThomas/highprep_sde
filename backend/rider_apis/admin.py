from django.contrib import admin
from .models import Bag


class LocationAdmin(admin.ModelAdmin):
    readonly_fields = ("bag_id",)



# Register your models here.
admin.site.register(Bag, LocationAdmin);
