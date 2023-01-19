from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# endpoint to return the lat-long of the places from the google maps 
class LatLongView(APIView):
    def get(self, request):
        return Response("This is api to return the latitute and longitude of the places that are given");





# endpoint to upload the excel sheet 
class UploadExcelSheetView(APIView):
    def post(self, request):

########################################################################################################
        # TODO 
            # 1. fetch the excel sheet from the frontend from warehouse guy 
            # 2. store this in database 
########################################################################################################


        return Response("endpoint to upload the excel sheet to store this in db")



# endpoint to start the algorithm once warehouse guy presses start algo 
class StartAlgoView(APIView):
    def get(self, request):
        
########################################################################################################
        # TODO
            # 1.fetch the excel sheet consisting of the list of places and the available rider 
            # 2. find the (lat, long) for each of the places, distance and time matrix using google maps apis
            # 3. then these points will be feed to the algorithm 
            # 4. wait for the algorithm to return the final result 
            # 5. once got the final result find the routes of each destination for each rider.
            # 6. store this in database.(why ??)
            # 7. then return the direction routes with rider id to the frontend or warehouse guy to be specific.
            # 8. also notify each rider about the directions routes that needs to be navigated.(this is the current issue how are we going to do that).
        # main problems will be to 

###########################################################################################################


        # implemeting for testing purpose by hardcoding
        # ridersVsLocations = {};
        # ridersVsLocations['1'] = 
        # lat = [12.91345, 12.94022, ]


        return Response("this endpoint is to start the algorithm to return the list of riders and their ordered set of locations");


