from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import PersonInfo
from .serializers import PersonInfoSerializer, PersonLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib import auth
from algo_apis.models import Rider


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
class PersonListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # if it is a get request then we have to show the list of person for this purpsoe 
    def get(self, request):

        personList = PersonInfo.objects.all();

        # serialize the data to convert this in json format 
        serializedData = PersonInfoSerializer(personList, many=True);

        # say everything went fine 
        return Response(serializedData.data);
    
    # if this is post then we have to create a new person 
    # this is the registration of the new person/user 
   


# end point to login the already existing user 
class PersonLoginView(APIView):
    def post(self, request):
        # TODO
        serializedDAta = PersonLoginSerializer(data=request.data);

        if serializedDAta.is_valid():
            email = serializedDAta.data.get('email');
            password = serializedDAta.data.get('password');
            # print("\n\n\n");
            # print(serializedDAta)
            # print(serializedDAta.data);
            # print("\n\n\n");
            print("the email is ", email);
            print("password is", password);
            # now we have to authenticate this user 
            currentUser = authenticate(email=email, password=password);
            # user = PersonInfo.objects.get(email = email);
            # print(user.name);
            # print(user.phone_number);
            # print(user.age);
            # print(user.password);
            # print("The another user is ", user);
            # print("The current user is \n\n");
            # print(currentUser);
            if currentUser is not None:
                print("Successfullt sent the response")
                return Response({'msg' : 'Login Success'}, status=status.HTTP_200_OK)
            else :
                return Response({'errors' : {'non_field_errors' : ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
            
            # say everything went fine 
            return Response(serializedDAta.errors, status=status.HTTP_400_BAD_REQUEST)
        pass


# end point to register the person in application for first time 
class PersonRegister(APIView):

     def post(self, request):
        # we have to serialize the data 
        data = request.data;

        serializedData = PersonInfoSerializer(data=data);

        # checking the validity of data 
        if serializedData.is_valid() :
            serializedData.save();
        else :
            return Response(serializedData.errors, status=status.HTTP_403_FORBIDDEN);
        print("The serialized data is\n\n ", serializedData);
        print("The serialized data with data  is\n\n ", serializedData.data);
        
        person = PersonInfo.objects.get(email = serializedData.data['email']);
        if person.person_type == "rider":
            # then we also have to store this information in the rider table as well 
            newRider = Rider(email = person.email, status = "NotAvailable", location_ids = {});
            newRider.save();
        
        # print("The new user which is registering is ==> \n\n\n", person);

        # we have to create the token for the first time 
        # refreshToken = RefreshToken.for_user(person);
        # accessToken = refreshToken.access_token;
        token, _ = Token.objects.get_or_create(user = person);
        # say everything went fine 
        return Response({'msg' : 'Registration Successfull','payload': serializedData.data, 'token' : str(token)}, status=status.HTTP_201_CREATED);
        # return Response({'msg' : 'Registration Successfull','payload': serializedData.data, 'refresh' : str(refreshToken), 'access' : str(accessToken)}, status=status.HTTP_201_CREATED);
        # return Response({'msg' : 'Registration Successfull','payload': serializedData.data}, status=status.HTTP_201_CREATED);

        # otherwise i will save this to the database 

class LogoutView(APIView):
    @staticmethod
    def delete(request, *args, **kwargs):
        auth.logout(request)
        data = {
            "message": "You have successfully logged out.",
        }
        return Response(data, status=status.HTTP_200_OK)


class randomView(APIView):
    def get(self, request):
        return Response("hello");
