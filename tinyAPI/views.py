from django.shortcuts import render
from django.http import HttpResponse
import numpy
import random
import datetime

from .modelBot import model as modelo

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import TinyResponseSerializer, CourseSerializer
# from rest_framework import viewsets

from . models import Question, Calendar, userIntent, Course
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def index(request):
    inp = 'hi'
    asnw = "blank"

    results = modelo.model.predict([modelo.bag_of_words(inp, modelo.words)])[0]
    results_index = numpy.argmax(results)
    tag = modelo.labels[results_index]

    if results[results_index] > 0.7:
        for tg in modelo.data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        asnw = random.choice(responses)
    else:
        asnw = "i hvae no response for that"
    # tiny_response = {'response': asnw}
    return HttpResponse(asnw)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def sendQuery(request, query):
    inp = query
    asnw = "blank"

    results = modelo.model.predict([modelo.bag_of_words(inp, modelo.words)])[0]
    results_index = numpy.argmax(results)
    tag = modelo.labels[results_index]

    if results[results_index] > 0.7:
        for tg in modelo.data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        asnw = random.choice(responses)
    else:
        asnw = "i hvae no response for that"
    tiny_response = {'response': asnw}

    if request.method == 'GET':

        # find if the query is in Question model
        if 'mod^' in tiny_response['response']:
            tiny_response = {'response': Question.objects.get(
                query=tiny_response['response']).answer}

        serializer = TinyResponseSerializer(tiny_response)
        return Response(serializer.data)


####################################Courses things#################################################

# get all courses
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def viewAllCourses(request):
    courses = Course.objects.all()

    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


# get course by college
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getCourseByCollege(request, college):
    courses = Course.objects.filter(college_acronym=college.upper())
    if courses.count() == 0:
        courses = Course.objects.filter(college__icontains=college)
    if courses.count() == 0:
        return Response({'Message': 'No Courses Found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


# delete course
@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def deleteCourse(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response({'Message': 'Id Not Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = course.delete()
        data = {}
        if operation:

            data["success"] = "delete successful"
        else:
            data["failed"] = "delete failed"

        return Response(data)


# add course
@api_view(['POST', ])
def addCourse(request, course_name, college, acronym, campus):
    try:
        newcourse = Course.objects.create(
            course=course_name,
            college=college,
            college_acronym=acronym,
            campus=campus
        )
        newcourse.save()
    except:
        return Response({'error': 'idk'})
    return Response({'Message': 'Succesfully added'})


####################################User things#################################################


@api_view(['POST', ])
def createUser(request, username, password, email, firstname, lastname, intent):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            first_name=firstname,
                                            last_name=lastname,
                                            password=password)
            intent = userIntent(intent=intent, user=user)

            intent.save()
        except:
            return Response({'error': 'Username is already taken'})

        intent.save()

    return Response({'message': "created success"})
    # http://127.0.0.1:8000/tinyAPI/createUser/dawn11232123/124553/dawnhae/school related/


@api_view(['GET', ])
def adminLogin(request, username, password):
    admin = authenticate(request, username=username, password=password)
    if admin is not None:
        if admin.is_staff:
            return Response({'result': 'found', 'username': username, 'password': password})

    return Response({'result': 'not found'})
    # http://127.0.0.1:8000/tinyAPI/adminLogin/kishinki/dawn123741/
