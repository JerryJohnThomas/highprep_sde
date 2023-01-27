from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response;
from rest_framework import status
from algo_apis.models import Rider
from algo_apis.serializers import RiderSerializer;
from login_apis.serializers import PersonInfoSerializer
from login_apis.models import PersonInfo
from .models import Bag
from inventory_apis.models import Item
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
            currentRiderJson = {
                "name" :  currentRider.name,
                "phone_number" : currentRider.phone_number,
                "age" : currentRider.age,
                "person_type" : currentRider.person_type,
                "bike_details" : currentRider.bike_details,
                "email" : currentRider.email
                
            }
            print(currentRiderJson);
            ridersList.append(currentRiderJson)
            
        return Response({"msg" : "Success", "data" : ridersList}, status=status.HTTP_200_OK);
    



# end point to give the details about the locations that has been assigned to the riders 
class RiderDropLocations(APIView):
    def get(self, request):
        # i just need the email of the riders and thats it 
        email = request.data["email"];

        print("The email of the rider is ", email);
        
        currentRider = Rider.objects.get(email = email);

        currentLocations = currentRider.location_ids;


        
        # say everything went fine 
        return Response({"msg": "success", "data" : currentLocations});



# end point to mark the location as complete 
class MarkRiderLocationAsMarked(APIView):
    # this will be a post request for this purpose 
    def post(self, request):
        # here i need to have the lat long which has been completed for this purpose 
        latitude = request.data["lat"];
        longitude = request.data["long"];
        email = request.data["email"];
        
        # we have to find the rider 
        currentRider = Rider.objects.get(email = email);
        coordinates = currentRider.location_ids["coordinates"];

        print(type(coordinates));

        # using the for loop for updating the new coordinates for this purpose 
        newCoordinates = [];

        for coordinate in coordinates:
            print("The current coordinate is \n");
            print(coordinate)
            # print(type(latitude))
            if float(latitude) in coordinate and float(longitude) in coordinate:
                continue;
            else :
                newCoordinates.append(coordinate);
        
        print("The number of coordinates are as follows \n\n")
        print(len(coordinates))

        print("The number of coordinates after marking one as complete is as follows \n");
        print(len(newCoordinates));
        
        # print("The remaining coordinates for this is as follows\n\n", coordinates);
        currentRider.location_ids["coordinates"] = newCoordinates; 
        
        currentRider.save();

        # say everything went fine 
        return Response({"msg" : "successfully marked it as complete", "data" : newCoordinates});




# end point to give the details about the items that he is taking inside the bag 
class RiderBagDetails(APIView):
    # this will be a get request 
    def get(self, request):
        currentRiderEmail = request.data["email"];

        currentRider = Rider.objects.get(email = currentRiderEmail);

        bag_id = currentRider.bag_id;

        if bag_id == "-1":
            # then this rider is not yet assigned a bag or it has not been assigned a 
            return Response({"msg" : "Rider has not assigned a bag"}, status=status.HTTP_200_OK);
        # now we have to search the bag with this bag_id 
        currentBag = Bag.objects.get(bag_id = int(bag_id));
        print("The current information about the bag is as follows\n\n", currentBag.item_list);
        bagDetailsJson = {
            "bag_id" : currentBag.bag_id,
            "bag_size" : currentBag.bag_size,
            "items_List" : currentBag.item_list
        }
        # say everything went fine 
        return Response({"msg" : "success", "data" : bagDetailsJson}, status=status.HTTP_200_OK);


# end point to mark the pickup location as complete for this purpose 
class MarkPickUpCompleted(APIView):
    # this will again be a post request 
    def post(self, request):
        
        # say everything went fine 
        return Response("end point for rider to mark the pickup location as complete");




# end point to create new bag 
class AddItemToRiderBag(APIView):
    # this will be a post request since we are adding the new bag for this purpose
    def post(self, request):
        # i need the list of items in order to create the new bag 
        email = request.data["email"];
        item = request.data["item"];

        # here we have to get the rider first 
        currentRider = Rider.objects.get(email = email);
        # now we have to find the id of bag and find the bag for this purpose 
        currentBag = Bag.objects.get(bag_id = int(currentRider.bag_id));

        currentItemList = currentBag.item_list["item"];
        print("The current bag list items is ", currentItemList);
        # here we have to append all the information of the items from the database for this purpose 
        currentItem = Item.objects.get(item_name = item);
        
        currentBag.item_list["item"].append(currentItem);
        print("After adding the item the list of items is ", currentBag.item_list);
        currentBag.save();

        


        # say everything went fine 
        return Response("successfully created the new bag");

# end point to remove the item from the bag for this purpose 