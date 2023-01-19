# this is the url file for the blog_api application 
from django.contrib import admin
from django.urls import path, include

from login_apis.views import PersonDetails,PersonListView, PersonLoginView, PersonRegister
app_name = 'login_apis'
urlpatterns = [
    # we will be making endpoints to get the post details 
    # endpoint to show a single item 
    path('<int:pk>/', PersonDetails.as_view(), name='PersonDetails'),
    # endpoint to show all the list items 
    # this end point is to register the user or else login the register if already exists.
    path('person/', PersonListView.as_view(), name='PersonLoginView'),
    # this end point to login the users 
    path('person/login/', PersonLoginView.as_view(), name='PersonLoginView'),
    path('person/register/', PersonRegister.as_view(), name='PersonRegister'),
    
]
