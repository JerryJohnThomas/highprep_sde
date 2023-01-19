from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import PersonInfo
from .serializers import PersonInfoSerializer

# Create your views here.
# endpoint to fetch the detail of a single person 
class PersonDetails(APIView):
    def get(self, request, pk):
        primaryKey = self.kwargs['pk'];

        currentPerson = PersonInfo.objects.filter(id = primaryKey);
        currentPerson = PersonInfoSerializer(currentPerson, many=True);


        print("The post after serialization is ", currentPerson.data);


        # say everything went fine 
        return Response(currentPerson.data);



# here i will be making the view for handling the login for this purpose 
class PersonLoginView(APIView):
    # if it is a get request then we have to show the list of person for this purpsoe 
    def get(self, request):
        personList = PersonInfo.objects.all();

        # serialize the data to convert this in json format 
        serializedData = PersonInfoSerializer(personList, many=True);

        # say everything went fine 
        return Response(serializedData.data);
    
    # if this is post then we have to create a new person 
    def post(self, request):
        # we have to serialize the data 
        data = request.data;

        serializedData = PersonInfoSerializer(data=data);

        # checking the validity of data 
        if serializedData.is_valid() :
            serializedData.save();
        else :
            return Response(serializedData.errors, status=status.HTTP_403_FORBIDDEN);
        
        # say everything went fine 
        return Response(serializedData.data, status=status.HTTP_201_CREATED);
