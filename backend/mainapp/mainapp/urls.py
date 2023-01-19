from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", include('login_api.urls')),
    # adding the new route to handle the apis of the google maps 
    path("start/", include('starting_apis.urls')),
    path("inventory/", include("inventory_apis.urls")),
]
