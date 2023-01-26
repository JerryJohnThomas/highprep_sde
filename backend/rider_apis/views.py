from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response;
from rest_framework import status
from algo_apis.models import Rider
from algo_apis.serializers import RiderSerializer;
from login_apis.serializers import PersonInfoSerializer
from login_apis.models import PersonInfo

# Create your views here.
# endpoint to get the list of riders under a given warehouse manager 
class RiderListView(APIView):
    # this is the get request 
    def get(self, request):
        warehouseManagerEmail = request.data['email'];
        print("The email of warehouse manager is ", warehouseManagerEmail);

        listOfRiders = Rider.objects.filter(username = warehouseManagerEmail);
        print(listOfRiders);

        ridersList = [];
        # using the for loop for this purpose 
        for rider in listOfRiders:
            currentRider = PersonInfo.objects.get(email = rider.email);
            serializedData = PersonInfoSerializer(data=currentRider)
        # we have to use the serializers for this purpose 
        serializedData = RiderSerializer(data=listOfRiders, many=True)

        if not serializedData.is_valid():
            return Response({"msg" : "Failed", "data" : serializedData.data})

        # print("The list of these riders is as follows \n\n", serializedData.data);
        Response({"msg" : "Success", "data" : serializedData.data}, status=status.HTTP_200_OK);
    



# end point to give the details about the locations that has been assigned to the riders 
class RiderDropLocations(APIView):
    def get(self, request):
        
        # say everything went fine 
        return Response("this is end point to send the riders location to the frontend for this purpose");



# end point to mark the location as complete 
class MarkRiderLocationAsMarked(APIView):
    # this will be a post request for this purpose 
    def post(self, request):
        # say everything went fine 
        return Response("done");




# end point to give the details about the items that he is taking inside the bad 
class RiderBagDetails(APIView):
    # this will be a get request 
    def get(self, request):
        # say everything went fine 
        return Response("this end point is to return the details about the bag for this purpose");

# end point to mark the pickup location as complete for this purpose 
class MarkPickUpCompleted(APIView):
    # this will again be a post request 
    def post(self, request):
        
        # say everything went fine 
        return Response("end point for rider to mark the pickup location as complete");
        
