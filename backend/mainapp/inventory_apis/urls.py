# this is urls for login_api to direct the route for logins of different users.
from django.contrib import admin
from django.urls import path, include

from inventory_apis.views import ListAllItemsView

app_name = 'inventory_apis'
urlpatterns = [
    path("", ListAllItemsView.as_view(), name='ListAllItemsView'),
]
