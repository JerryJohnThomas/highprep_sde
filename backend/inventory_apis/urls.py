# this is the url file for the blog_api application 
from django.contrib import admin
from django.urls import path, include

from inventory_apis.views import ItemDetails, ItemList
app_name = 'inventory_apis'
urlpatterns = [
    # we will be making endpoints to get the post details 
    # endpoint to show a single item 
    path('<int:pk>/', ItemDetails.as_view(), name='ItemDetails'),
    # endpoint to show all the list items 
    path('', ItemList.as_view(), name='ItemCreate'),
]
