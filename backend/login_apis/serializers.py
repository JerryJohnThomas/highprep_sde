# here we have to make the serializer for person information 

from rest_framework import serializers;
from .models import PersonInfo;


# defining the post serializer 
class PersonInfoSerializer(serializers.ModelSerializer):


    # adding the extra field to have the confirm password field as well for this purpose 
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only = True);
    class Meta:
        # here i am saying that this serializer is for the post model
        model = PersonInfo;
        # and in the field section we are saying that we want to show all the fields in the api 
        fields = "__all__";


    # implementing the validation method for checking whether the credentials are correct or not 
    def validate(self, attrs):
        password = attrs.get('password');
        password2 = attrs.get('password2');

        if password != password2:
            raise serializers.ValidationError("The password didnot matched");

        return attrs

    # defining the function to create the user  or to save the user 
    def create(self, validated_data):
        # say everything went fine 
        return PersonInfo.objects.create_user(**validated_data)        
