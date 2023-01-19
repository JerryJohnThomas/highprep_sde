# this is urls for login_api to direct the route for logins of different users.
from django.contrib import admin
from django.urls import path, include

from login_api.views import AdminLoginView
from starting_apis.views import LatLongView, UploadExcelSheetView
from starting_apis.views import StartAlgoView

app_name = 'starting_apis'

urlpatterns = [
    path("coordinates/", LatLongView.as_view(), name='LatLongView'),
    path("algo/", StartAlgoView.as_view(), name='StartAlgoView'),
    # endpoint to add the excel sheet 
    path("upload/", UploadExcelSheetView.as_view(), name="UploadExcelSheetView"),
]
