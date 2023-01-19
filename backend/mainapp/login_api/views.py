from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status;

from login_api.serializers import PersonalInfoSerializer
from login_api.models import PersonalInfo

# Create your views here.
class AdminLoginView(APIView):

    # get request to sign up the admin 
    def get(self, request):
        personal_info_list = PersonalInfo.objects.all();

        serializedData = PersonalInfoSerializer(personal_info_list, many=True);

        # return Response(serializedData.data);
        return Response(serializedData.data);
        
        # return Response("This is api to register the admin after verifying the credentials");
    def post(self, request):
        # data = request.data;
        # we have to serialize the data 
        print("The request.data", request.data['name']);
        serializedData = PersonalInfoSerializer(data=dict(request.data));
        print("The serialized data is as follows\n", serializedData);

        #     "name" : "rupesh kumar",
        # "username" : "rupeshkumar",
        # "password" : "123",
        # "age" : 21,
        # "phone_number" : "1234567890",
        # "person_type" : "customer",
        # "bike_details" : "some bike details"


        if serializedData.is_valid() :
            serializedData.save();
        else:
            return Response(serializedData.errors, status=status.HTTP_403_FORBIDDEN)

        datas = serializedData.data
        print("the datas are as follows\n", datas);
        # print("the data from the backend is ", data);
        # return Response(serializedData.data, status=status.HTTP_201_CREATED);
        return Response({"status": "success", "data": serializedData.data}, status=status.HTTP_200_OK);
        # return Response("some random data ");