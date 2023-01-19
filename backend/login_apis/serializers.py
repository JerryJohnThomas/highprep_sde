# here we have to make the serializer for person information 

from rest_framework import serializers;
from .models import PersonInfo;


# defining the post serializer 
class PersonInfoSerializer(serializers.ModelSerializer):

    class Meta:
        # here i am saying that this serializer is for the post model
        model = PersonInfo;
        # and in the field section we are saying that we want to show all the fields in the api 
        fields = "__all__";

        