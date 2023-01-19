from rest_framework import serializers;
from login_api.models import PersonalInfo;


# # defining the post serializer 
class PersonalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        # here i am saying that this serializer is for the post model
        model = PersonalInfo;
        # and in the field section we are saying that we want to show all the fields in the api 
        # fields = ("name", "username");
        fields = ("name", "username", "bike_details", "phone_number");

# from rest_framework import serializers;
# from blog.models import Post;


# # defining the post serializer 
# class PostSerializer(serializers.ModelSerializer):

#     class Meta:
#         # here i am saying that this serializer is for the post model
#         model = Post;
#         # and in the field section we are saying that we want to show all the fields in the api 
#         fields = "__all__";
