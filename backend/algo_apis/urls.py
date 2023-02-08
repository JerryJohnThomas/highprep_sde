# this is urls for login_api to direct the route for logins of different users.
from django.contrib import admin
from django.urls import path, include


from algo_apis.views import LatLongView, UploadExcelSheetView
from algo_apis.views import StartAlgoView, StatusOfAlgo, FastForward, DynamicPickUpPoints, CvPoint, DummyStart
# , StartAlgoView2


app_name = 'algo_apis'

urlpatterns = [
    path("coordinates/", LatLongView.as_view(), name='LatLongView'),
    path("start/", StartAlgoView.as_view(), name='StartAlgoView'),
    # path("starttest/", StartAlgoView2.as_view(), name='StartAlgoView2'),
    # endpoint to add the excel sheet 
    path("upload/", UploadExcelSheetView.as_view(), name="UploadExcelSheetView"),
    path("status/", StatusOfAlgo.as_view(), name="StatusOfAlgo"),
    path("fastforward/", FastForward.as_view(), name="FastForward"),
    path("dynamicpickup/", DynamicPickUpPoints.as_view(), name="DynamicPickUpPoints"),
    path("cv/", CvPoint.as_view(), name="CvPoint"),
    path("dummystart/", DummyStart.as_view(), name="DummyStart"),

]
