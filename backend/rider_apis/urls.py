# this is urls for login_api to direct the route for logins of different users.
from django.contrib import admin
from django.urls import path, include

from rider_apis.views import RiderListView, RiderDropLocations, MarkRiderLocationAsMarked, AddItemToRiderBag
from rider_apis.views import RiderBagDetails

app_name = 'rider_apis'

urlpatterns = [
    path("", RiderListView.as_view(), name='RiderListView'),
    path("locations/", RiderDropLocations.as_view(), name="RiderDropLocations"),
    path("complete/", MarkRiderLocationAsMarked.as_view(), name="MarkRiderLocationAsMarked"),
    path("additem/", AddItemToRiderBag.as_view(), name="AddItemToRiderBag"),
    path("bagdetails/", RiderBagDetails.as_view(), name = "RiderBagDetails"),
    
]
