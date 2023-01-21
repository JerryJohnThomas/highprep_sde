# here i will be making the serializer in order to serialize the data that we get from the database or client side 

from rest_framework import serializers;
from .models import Item;


# defining the post serializer 
class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        # here i am saying that this serializer is for the post model
        model = Item;
        # and in the field section we are saying that we want to show all the fields in the api 
        fields = "__all__";

        