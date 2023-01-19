from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemSerializer
from .models import Item;

# Create your views here.
class ListAllItemsView(APIView):
    def get(self, request):
        list_of = Item.objects.all();
        serializedData = ItemSerializer(list_of, many=True);


        return Response(serializedData.data);
    def post(self, request):
        serializedData = ItemSerializer(data=(request.data));
        print("The serialized data is as follows\n\n\n\n", serializedData);

        if serializedData.is_valid():
            serializedData.save();
        else :
                return Response(serializedData.errors);
        print("The data that i got is \n\n", serializedData.data)
        return Response(serializedData.data);
