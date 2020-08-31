from rest_framework import serializers
from .models import Course, Executive, Dean, Population, Random
from django.contrib.auth.models import User

# class TinyResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TinyResponse
#         fields = ['response', ]


class TinyResponseSerializer(serializers.Serializer):
    response = serializers.CharField(max_length=100)

    def create(self, TinyResponseSerializer):
        return TinyResponseSerializer.objects.create(self.response)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ExecutiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executive
        fields = '__all__'


class DeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dean
        fields = '__all__'


class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = '__all__'


class RandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Random
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class CourseByCollegeSerializer(serializers.Serializer):
#     response = serializers.CharField(max_length=500)

#     def create(self, CourseByCollegeSerializer):
#         return CourseByCollegeSerializer.objects.create(self.response)
