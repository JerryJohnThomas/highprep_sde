from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializer import ItemSerializer


# api to find the details of a single item in inventory 
class ItemDetails(APIView):
    def get(self, request, pk):

        primaryKey = self.kwargs['pk'];
        
        print("The user has made the get request to get the details about the post \n");
        print("The primary key for the post is ", primaryKey);


        # we have to fetch this data from the database and put it in the serialzer for this purpose 
        currentItem = Item.objects.filter(id = primaryKey);
        currentItem = ItemSerializer(currentItem, many=True);
        print("The post after serialization is ", currentItem.data);

        # send the response to frontend 
        return Response(currentItem.data);




    
# view to show the list of items that are present and to add new list if it is post request 
class ItemList(APIView):

    # handling the get request 
    def get(self, request):

        itemList = Item.objects.all();

        serializedData = ItemSerializer(itemList, many=True);
      
        return Response(serializedData.data);
        
    # handling the post request to create the new item in inventory 
    def post(self, request):
        serializedData = ItemSerializer(data=request.data);

        # now we have to save it 
        if serializedData.is_valid() :
            serializedData.save();
        else:
            return Response(serializedData.errors, status=status.HTTP_400_BAD_REQUEST);

        # sending a positive response to frontend in json format 
        return Response(serializedData.data, status=status.HTTP_201_CREATED);
