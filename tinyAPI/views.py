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
from rest_framework.authtoken.models import Token
from .serializers import TinyResponseSerializer, CourseSerializer, ExecutiveSerializer, DeanSerializer, PopulationSerializer, RandomSerializer, UserSerializer, ActionSerializer, CalendarSerializer, AuthTokenSerializer
# from rest_framework import viewsets

from . models import Question, Calendar, userIntent, Course, Executive, Dean, Population, Random, Action
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def index(request):
    inp = 'hi'
    asnw = "blank"

    results = modelo.model.predict([modelo.bag_of_words(inp, modelo.words)])[0]
    results_index = numpy.argmax(results)
    tag = modelo.labels[results_index]

    if results[results_index] > 0.95:
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
            return Executive.objects.filter(position__iexact=response[1])[0].name
        except:
            print("something is wrong")

    elif response[0] == 'deans':
        try:
            return Dean.objects.filter(college__iexact=response[1])[0].name
        except:
            print("something is wrong")

    elif response[0] == 'populations':
        try:
            return Population.objects.filter(college__iexact=response[1])[0].student_population
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
            cals = Calendar.objects.filter(event=target)

            for cal in cals:
                if cal.date_start <= use_date and cal.date_end >= use_date:
                    return cal.remark
        except:
            return "theres no yet announcement from BulSU administration"

    if (target == 'midterm' or target == 'finals'
            or target == 'entrance_exam' or target == 'sem_open' or target == 'sem_end'):
        try:
            # .date_start.year
            cals = Calendar.objects.filter(event=target)

            for cal in cals:
                if cal.date_start.year == today.year and cal.date_start > today:
                    print(cal.remark)
                    return cal.remark
        except:
            return "theres no yet announcement from BulSU administration"

    return 'No update yet...'


def addAction(transaction):
    new_action = Action.objects.create(
        action=transaction
    )
    new_action.save()


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def sendQuery(request):
    inp = request.data['message']
    asnw = "blank"

    results = modelo.model.predict([modelo.bag_of_words(inp, modelo.words)])[0]
    results_index = numpy.argmax(results)
    tag = modelo.labels[results_index]
    ##adjust 
    # print("see level: "+results[results_index])
    if results[results_index] > 0.97:
        for tg in modelo.data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        asnw = random.choice(responses)
    else:
        asnw = "i hvae no response for that"
    tiny_response = {'response': asnw}

    if request.method == 'POST':

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
            
            token = Token.objects.get(user=user)
            return Response({
                "token": token.key,
                'user': token.user.username,
                'message': "created success"
                })
        except:
            return Response({'error': 'Username is already taken'})
        

    
    # http://127.0.0.1:8000/tinyAPI/createUser/dawn12/124553/dawnhae.gmail.com/dawn/bugay/school related/

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def getTokenUsers(request):

    token = Token.objects.all()

    serializer = AuthTokenSerializer(token, many=True)
    return Response(serializer.data)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getUsers(request):
    users = User.objects.all()

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)




####################################Admin routes#################################################
#admin login
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def adminLogin(request, username, password):
    admin = authenticate(request, username=username, password=password)
    if admin is not None:
        if admin.is_staff:
            return Response({'result': 'found', 'username': username, 'password': password})

    return Response({'MESSAGE': 'Invallid Credential'}, status=status.HTTP_404_NOT_FOUND)
    # http://127.0.0.1:8000/tinyAPI/adminLogin/kishinki/dawn123741/


#edit username
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def updateUsername(request, oldusername, newusername, password):
    admin = authenticate(request, username=oldusername, password=password)
    if admin is not None:
        if admin.is_staff:
            User.objects.filter(is_staff= True).update(username=newusername)
            updatedadmin = User.objects.get(is_staff=True)
            addAction("Updated username")
            return Response({'id': updatedadmin.id, 'new_username': updatedadmin.username})

    return Response({'result': 'not found'})   


#edit password
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def updatePassword(request, username, password, newpassword):
    admin = authenticate(request, username=username, password=password)
    if admin is not None:
        if admin.is_staff:
            user = User.objects.get(is_staff= True)
            user.set_password(newpassword)
            user.save()
            updatedadmin = User.objects.get(is_staff=True)
            addAction("Updated password")
            return Response({'id': updatedadmin.id,  'new_password': updatedadmin.password})

    # u = User.objects.get(is_staff= True)
    # u.set_password('dawn12374')
    # u.save()
    return Response({'result': 'not found'})

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def getActions(request):
    actions = Action.objects.all().order_by('-id')
    serializer = ActionSerializer(actions, many=True)
    return Response(serializer.data)



####################################End points#################################################


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getExecutives(request):
    executive = Executive.objects.all().order_by('id')

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
    dean = Dean.objects.all().order_by('id')

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
    population = Population.objects.all().order_by('id')

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
    random = Random.objects.all().order_by('id')

    serializer = RandomSerializer(random, many=True)
    return Response(serializer.data)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
def updateRandom(request, id):
    try:
        answer = request.data['answer']
        Random.objects.filter(id=id).update(
            answer=answer)
        random = Random.objects.get(id=id)

        return Response({'id': random.id, 'key': random.key, 'answer': random.answer, 'question': random.question})
    except:
        return Response({'MESSAGE': 'ID NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)


######################calendar routes#################
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getAllCalendar(request):
    calendar = Calendar.objects.all().order_by("-id")

    serializer = CalendarSerializer(calendar, many=True)
    return Response(serializer.data)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getAllHolidays(request):
    holidays = Calendar.objects.filter(event="holiday")
    data=[]
    for holiday in holidays:
        data.append({
            "date_start": holiday.date_start,
            "date_end": holiday.date_end,
            "event": holiday.event,
            "remark": holiday.remark,
            "name": holiday.name
            }
        )
    print(data)

    return Response(data)

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def addCalendarEvent(request, event, date_start, date_end, remark, name, color):
    try:
        new_event = Calendar.objects.create(
            event=event,
            date_start= date_start,
            date_end= date_end,
            remark=remark,
            name= name,
            color=color
            )
        calendar = Calendar.objects.all().order_by("-id")

        serializer = CalendarSerializer(calendar, many=True)
        return Response(serializer.data)
    except:
        return Response({'MESSAGE': 'unsuccess'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
def updateCalendarEvent(request, id, remark):
    try:
        Calendar.objects.filter(id=id).update(
            remark=remark
             )
        calendar = Calendar.objects.get(id=id)

        return Response({'id': calendar.id, 
        'remark': calendar.remark, 
        'event': calendar.event,
        'date_start': calendar.date_start,
        'date_end': calendar.date_end,
        "name": calendar.name,
        "color": calendar.color
        })
    except:
        return Response({'MESSAGE': 'unsuccess'}, status=status.HTTP_404_NOT_FOUND)

#create delete calendar event

@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def deleteCalendarEvent(request, id):
    try:
        event = Calendar.objects.get(id=id)
        event.delete()
        return Response({'MESSAGE': 'SUCCESSFULLLY DELETED'})
    except:
        return Response({'MESSAGE': 'unseccess'}, status=status.HTTP_404_NOT_FOUND)




#################################auth#################################

# @api_view(['GET',])
# @permission_classes((IsAuthenticated,))
# def getAllToken
