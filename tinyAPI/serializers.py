from rest_framework import serializers
from .models import Course

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


# class CourseByCollegeSerializer(serializers.Serializer):
#     response = serializers.CharField(max_length=500)

#     def create(self, CourseByCollegeSerializer):
#         return CourseByCollegeSerializer.objects.create(self.response)
