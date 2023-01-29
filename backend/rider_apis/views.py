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



# defining the function to remove the item from the list for this purpose 
def removeItemFromBag(currentRider, index):
    print("The current rider is ", currentRider);
    print("The current bag id is ", type(currentRider.bag_id))
    print("The current bag id is ", (currentRider.bag_id))

    bag_id = int(currentRider.bag_id);
    print("The bag_id for this rider is \n", bag_id);

    currentBag = Bag.objects.get(bag_id = bag_id);

    print("The list of items of items in this bag is ", currentBag.item_list["item"]);
    print('The length of this item list is \n', len(currentBag.item_list["item"]));

    # deleting this item at this particular index 
    del currentBag.item_list["item"][index];
    # saving this change 
    currentBag.save();

    print("the updated list of items is as follows \n", currentBag.item_list["item"]);
    print("The length after deletion of one item from the bag is as follows \n", len(currentBag.item_list["item"]));


    # say everything went fine 
    return currentBag;


# end point to mark the location as complete 
class MarkRiderLocationAsMarked(APIView):
    # this will be a post request for this purpose 
    # whenever we are marking this location as complete then we need to delete the location from location_ids 
    # and also we have to delete the item from the assigned bag for this particular rider 
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
        index = -1;
        k = 0;
        for coordinate in coordinates:
            print("The current coordinate is \n");
            print(coordinate)
            # print(type(latitude))
            if float(latitude) in coordinate and float(longitude) in coordinate:
                index = k;
                continue;
            else :
                newCoordinates.append(coordinate);
            k = k+1;
        
        # now i also have to remove the element from the bag list as well for this purpose 

        print("The number of coordinates are as follows \n\n")
        print(len(coordinates))

        print("The number of coordinates after marking one as complete is as follows \n");
        print(len(newCoordinates));
        
        # print("The remaining coordinates for this is as follows\n\n", coordinates);
        currentRider.location_ids["coordinates"] = newCoordinates; 
        
        currentRider.save();
        currentBag = removeItemFromBag(currentRider, index);

        # say everything went fine 
        return Response({"msg" : "successfully marked it as complete", "data" : newCoordinates, "bag"  : currentBag.item_list["item"]});




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
        currentItemJson = {
            "item_name" : currentItem.item_name, 
            "item_volume" : currentItem.item_volume
        }
        currentBag.item_list["item"].append(currentItemJson);
        print("After adding the item the list of items is ", currentBag.item_list);
        currentBag.save();

        


        # say everything went fine 
        return Response("successfully added the new item in bag");

# end point to remove the item from the bag for this purpose 