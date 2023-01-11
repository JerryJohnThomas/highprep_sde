from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class AdminLoginView(APIView):
    def get(self, request):
        return Response("This is api to login the admin after verifying the credentials");
