from rest_framework import serializers;
from .models import Item;


# # defining the post serializer 
class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        # here i am saying that this serializer is for the post model
        model = Item;
        fields = ["item_name", "item_volume"];
        # and in the field section we are saying that we want to show all the fields in the api 
        # fields = ("name", "username");
        # fields = ("name", "username", "bike_details", "phone_number");

# from rest_framework import serializers;
# from blog.models import Post;


# # defining the post serializer 
# class PostSerializer(serializers.ModelSerializer):

#     class Meta:
#         # here i am saying that this serializer is for the post model
#         model = Post;
#         # and in the field section we are saying that we want to show all the fields in the api 
#         fields = "__all__";
