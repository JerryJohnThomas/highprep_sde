
from rest_framework import serializers;
# from .models import PersonInfo;
from .models import AlgorithmStatusModel


# class RiderSerializer(serializers.Serializer):
#     class Meta:

class AlgorithmStatusModelSerializer(serializers.Serializer):
    class Meta:
        model = AlgorithmStatusModel
        fields = ("id", 'username', 'random_number', 'status', 'excelSheetFile')
    
    # def create(self, validated_data):
    #     return AlgorithmStatusModel.objects.create(**validated_data)