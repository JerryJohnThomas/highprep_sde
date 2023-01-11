# this is urls for login_api to direct the route for logins of different users.
from django.contrib import admin
from django.urls import path, include

from login_api.views import AdminLoginView

urlpatterns = [
    path("admin/", AdminLoginView.as_view(), name='AdminLoginView'),
]
