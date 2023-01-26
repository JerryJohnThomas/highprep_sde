# this is urls for login_api to direct the route for logins of different users.
from django.contrib import admin
from django.urls import path, include

from rider_apis.views import RiderListView

app_name = 'rider_apis'

urlpatterns = [
    path("", RiderListView.as_view(), name='RiderListView'),
    
]
