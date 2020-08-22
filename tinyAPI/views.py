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
from .serializers import TinyResponseSerializer, CourseSerializer, ExecutiveSerializer, DeanSerializer, PopulationSerializer, RandomSerializer
# from rest_framework import viewsets

from . models import Question, Calendar, userIntent, Course, Executive, Dean, Population, Random
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


def findInDatabase(response, userInput):
    response = response.split("^")
    print("workiiiiiiiiiiiiiiing")

    if response[0] == 'executives':
        try:
            return Executive.objects.get(position=response[1]).name
        except:
            print("something is wrong")

    elif response[0] == 'deans':
        try:
            return Dean.objects.get(college=response[1]).name
        except:
            print("something is wrong")

    elif response[0] == 'populations':
        try:
            return Population.objects.get(college=response[1]).student_population
        except:
            print("something is wrong")

    elif response[0] == 'random':
        try:
            return Random.objects.get(key=response[1]).answer
        except:
            print("something is wrong")

    elif response[0] == 'calendar':
        return findCalendar(response[1], userInput)


def findCalendar(target, userInput):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    use_date = tomorrow if 'TOM' in userInput.upper() else today

    if target == 'cancel' or target == 'holiday':
        try:
            cals = Calendar.objects.filter(
                Q(event='cancel') | Q(event='holiday'))

            for cal in cals:
                if cal.date_start <= use_date and cal.date_end >= use_date:
                    return cal.remark
        except:
            print("something is wrong")

    if (target == 'midterm' or target == 'finals'
            or target == 'entrance_exam' or target == 'sem_open' or target == 'sem_end'):
        try:
            # .date_start.year
            cals = Calendar.objects.filter(event=target)

            for cal in cals:
                if cal.date_start.year == today.year:
                    return cal.remark
        except:
            print("something is wrong")

    return 'No update yet...'


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
        if '^' in tiny_response['response']:
            tiny_response = {'response': findInDatabase(
                tiny_response['response'], inp)}

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


####################################End points#################################################


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getExecutives(request):
    executive = Executive.objects.all()

    serializer = ExecutiveSerializer(executive, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def updateExecutive(request, id, name):
    try:
        Executive.objects.filter(id=id).update(name=name)
        executive = Executive.objects.get(id=id)

        return Response({'id': executive.id, 'position': executive.position, 'name': executive.name})
    except:
        return Response({'MESSAGE': 'ID NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getDean(request):
    dean = Dean.objects.all()

    serializer = DeanSerializer(dean, many=True)
    return Response(serializer.data)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
def updateDean(request, id, name):
    try:
        Dean.objects.filter(id=id).update(name=name)
        dean = Dean.objects.get(id=id)

        return Response({'id': dean.id, 'college': dean.college, 'name': dean.name})
    except:
        return Response({'MESSAGE': 'ID NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getPopulation(request):
    population = Population.objects.all()

    serializer = PopulationSerializer(population, many=True)
    return Response(serializer.data)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
def updatePopulation(request, id, student_population):
    try:
        Population.objects.filter(id=id).update(
            student_population=int(student_population))
        population = Population.objects.get(id=id)

        return Response({'id': population.id, 'college': population.college, 'student_population': population.student_population})
    except:
        return Response({'MESSAGE': 'ID NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getRandom(request):
    random = Random.objects.all()

    serializer = RandomSerializer(random, many=True)
    return Response(serializer.data)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
def updateRandom(request, id, answer):
    try:
        Random.objects.filter(id=id).update(
            answer=answer)
        random = Random.objects.get(id=id)

        return Response({'id': random.id, 'key': random.key, 'answer': random.answer})
    except:
        return Response({'MESSAGE': 'ID NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
