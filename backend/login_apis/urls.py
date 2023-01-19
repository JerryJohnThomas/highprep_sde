# this is the url file for the blog_api application 
from django.contrib import admin
from django.urls import path, include

from login_apis.views import PersonDetails, PersonLoginView
app_name = 'login_apis'
urlpatterns = [
    # we will be making endpoints to get the post details 
    # endpoint to show a single item 
    path('<int:pk>/', PersonDetails.as_view(), name='PersonDetails'),
    # endpoint to show all the list items 
    path('hubmanager/', PersonLoginView.as_view(), name='PersonLoginView'),
]
