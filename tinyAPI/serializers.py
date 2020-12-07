from rest_framework import serializers
from .models import Course, Executive, Dean, Population, Random, Action, Calendar, ChatbotSettings, Contact
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework_recaptcha.fields import ReCaptchaField

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


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'



class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class ChatbotSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotSettings
        fields = '__all__'


class MySerializer(serializers.Serializer):
    recaptcha = ReCaptchaField(write_only=True)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


# class MyReCaptchaField(ReCaptchaField):
#     default_error_messages = {
#         "invalid-input-response": "reCAPTCHA token is invalid.",
#     }

# class CourseByCollegeSerializer(serializers.Serializer):
#     response = serializers.CharField(max_length=500)

#     def create(self, CourseByCollegeSerializer):
#         return CourseByCollegeSerializer.objects.create(self.response)
