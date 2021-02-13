from django.shortcuts import render
from django.http import HttpResponse
import numpy
import random
import datetime
import uuid

from .modelBot import model as modelo

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import TinyResponseSerializer, CourseSerializer, ExecutiveSerializer, DeanSerializer, PopulationSerializer, RandomSerializer, UserSerializer, ActionSerializer, CalendarSerializer, AuthTokenSerializer, ChatbotSettingsSerializer, MySerializer, ContactSerializer
# from rest_framework import viewsets

from . models import Question, Calendar, userIntent, Course, Executive, Dean, Population, Random, Action, ChatbotSettings, Contact, BetaTest
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


def my_random_string(string_length=10):
    random = str(uuid.uuid4()) 
    random = random.upper() 
    random = random.replace("-","") 
    return random[0:string_length] 


def findInDatabase(response, userInput):
    response = response.split("^")
    print("workiiiiiiiiiiiiiiing")

    if response[0] == 'executives':
        try:
            result = Executive.objects.filter(position__iexact=response[1])[0]
            name = result.name
            position = result.position
            return "The BulSU {} is {}".format(position, name)
        except:
            print("something is wrong")

    elif response[0] == 'deans':
        try:
            result = Dean.objects.filter(college__iexact=response[1])[0]
            name = result.name
            college = result.college
            return "The dean of {} is {}".format(college, name)
        except:
            print("something is wrong")

    elif response[0] == 'populations':
        try:
            result = Population.objects.filter(college__iexact=response[1])[0]
            student_population = result.student_population
            college = result.college
            return "The population of the student in {} is {} students".format(college, student_population)
        except:
            print("something is wrong")

    elif response[0] == 'random':
        try:
            return Random.objects.get(key=response[1]).answer
        except:
            print("something is wrong")

    elif response[0] == 'calendar':
        return findCalendar(response[1], userInput)

    elif response[0] == 'Contacts':
        try:
            result = Contact.objects.filter(ref__iexact=response[1])[0]
            
            office_name = result.office_name
            email = result.email
            facebook = result.facebook
            landline = result.landline
            college_secretary = result.college_secretary

            res = "You can contact {} via: <br/><br/>".format(office_name)
            if email !="":
                res+="Email: {} <br/>".format(email)
            if facebook !="":
                res+="Facebook: {} <br/>".format(facebook)
            if landline != "":
                res+="Deans Office Tel#: {} <br/>".format(landline)
            if college_secretary !="":
                res+="College Secretary Tel#: {}".format(college_secretary)
            
            return res
        except:
            print("something is wrong")




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
            #if holiday tommorow asking if cancelled
            if target == 'cancel' and (use_date == tomorrow or use_date == today):
                cals = Calendar.objects.filter(event='holiday')

                for cal in cals:
                    if cal.date_start <= use_date and cal.date_end >= use_date:
                        return cal.remark




        except:
            return "There is no yet announcement from the administration of BulSU."

    if (target == 'midterm' or target == 'finals'
            or target == 'entrance_exam' or target == 'sem_open' or target == 'sem_end'):
        try:
            # .date_start.year
            cals = Calendar.objects.filter(event=target)
            temp=""
            for cal in cals:
                if cal.date_start.year == today.year and cal.date_end >= today:
                    if temp == "":
                        temp = cal
                    elif temp.date_end > cal.date_end:
                        temp = cal
                    print(cal.remark)
            return temp.remark
        except:
            return "theres no yet announcement from BulSU administration"

    return random.choice(['No update yet...',"There is no yet announcement from the BulSU administration" ])


def addAction(transaction):
    new_action = Action.objects.create(
        action=transaction
    )
    new_action.save()


def displayLandline(college):
        try:
            contact = Contact.objects.get(office_name=college)
            return "If you want to get help in your concern you may contact {} at {}".format(college, contact.landline) if  contact.landline !="" else ""
        except:
            return ""


def unidentifyAnswer(sentence):
    if "CICT " in sentence.upper():
        landline = displayLandline("College of Information and Communications Technology")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CAFA " in sentence.upper():
        landline = displayLandline("College of Architecture and Fine Arts")
        return "Sorry, I don't understand. {}".format(landline)
    elif "LAW " in sentence.upper():
        landline = displayLandline("College of Law")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CAL " in sentence.upper():
        landline = displayLandline("College Of Arts And Letters")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CBA " in sentence.upper():
        landline = displayLandline("College of Business Administration")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CCJE " in sentence.upper():
        landline = displayLandline("College of Criminal Justice Education")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CHTM " in sentence.upper():
        landline = displayLandline("College of Hospitality and Tourism Management")
        return "Sorry, I don't understand. {}".format(landline)
    elif "COE " in sentence.upper():
        landline = displayLandline("College of Engineering")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CIT " in sentence.upper():
        landline = displayLandline("College of Industrial Technology")
        return "Sorry, I don't understand. {}".format(landline)
    elif "COED " in sentence.upper():
        landline = displayLandline("College of Education")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CON " in sentence.upper():
        landline = displayLandline("College of Nursing")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CS " in sentence.upper():
        landline = displayLandline("College of Science")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CSER " in sentence.upper():
        landline = displayLandline("College of Sports, Exercise and Recreation")
        return "Sorry, I don't understand. {}".format(landline)
    elif "CSSP " in sentence.upper():
        landline = displayLandline("College of Social Science And Philosophy")
        return "Sorry, I don't understand. {}".format(landline)
    elif "GRADUATE SCHOOL" in sentence.upper():
        landline = displayLandline("Graduate School")
        return "Sorry, I don't understand. {}".format(landline)
    elif "Admission" in sentence.upper():
        landline = displayLandline("Admission Office")
        return "Sorry, I don't understand. {}".format(landline)
    elif "MIS" in sentence.upper():
        landline = displayLandline("MIS Office")
        return "Sorry, I don't understand. {}".format(landline)
    elif "REGISTRAR" in sentence.upper():
        landline = displayLandline("Registrar Office")
        return "Sorry, I don't understand. {}".format(landline)
    elif "ACCOUNTING" in sentence.upper():
        landline = displayLandline("Accounting Office")
        return "Sorry, I don't understand. {}".format(landline)
    elif "SCHOLAR" in sentence.upper():
        landline = displayLandline("Scholar Office")
        return "Sorry, I don't understand. {}".format(landline)
    else:
        return "Sorry, I don't understand."

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def sendQuery(request):
    inp = request.data['message']
    asnw = "blank"

    results = modelo.model.predict([modelo.bag_of_words(inp, modelo.words)])[0]
    results_index = numpy.argmax(results)
    tag = modelo.labels[results_index]
    ##adjust 
    print("see level: {}".format(results[results_index]))
    if results[results_index] > 0.999: #97 dati yan ##98
        print("Percentage: {}".format(results[results_index]))
        for tg in modelo.data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        asnw = random.choice(responses)
    else:
        asnw = unidentifyAnswer(inp)
        # asnw = random.choice(["Sorry I can't understand you.", "Sorry, I don't understand"])
        BetaTest.objects.create(
            message=inp,
            accuracy=results[results_index]
        )
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
    courses = Course.objects.all().order_by('-id')

    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


# get course by college
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getCourseByCollege(request, college):
    courses = Course.objects.filter(college_acronym=college.upper())
    # if courses.count() == 0:
    #     courses = Course.objects.filter(college__icontains=college)
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
def addCourse(request,):
    course_name = request.data["course"]
    college = request.data["college"]
    campus = request.data["campus"]
    acronym = request.data["acronym"]
    print(request.data["campus"])


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

        find_user = User.objects.filter(email__iexact=email)

        if len(find_user) == 0:
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
                return Response({'error': 'server error'})
        else:
            return Response({'error': 'Email is already taken'})
            

    
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


@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def deleteUser(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response({'MESSAGE': 'SUCCESSFULLLY DELETED'})
    except:
        return Response({'MESSAGE': 'unseccess'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def tryCaptcha(request):
    token = request.data["captcha"]
    data = {"recaptcha": token}
    serializer = MySerializer(data=data)
    if serializer.is_valid():
        return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####################################Admin routes#################################################
#admin login
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def adminLogin(request):
    username = request.data["username"]
    password = request.data["password"]
    token = request.data["captcha"]
    data = {"recaptcha": token}
    serializer = MySerializer(data=data)

    captcha_response = False

    if serializer.is_valid():
        captcha_response = True
    else:
        captcha_response = serializer.errors

    admin = authenticate(request, username=username, password=password)
    if admin is not None:
        if admin.is_staff:
            return Response({'result': 'found', 'username': username, 'password': password, 'captcha_response': captcha_response})

    return Response({'MESSAGE': 'Invallid Credential', "captcha_response": captcha_response}, status=status.HTTP_404_NOT_FOUND)
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
def updatePassword(request):
    username = request.data["username"]
    password = request.data["oldpassword"]
    newpassword = request.data["newpassword"]

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


import smtplib
from email.message import EmailMessage

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def forgetPassword(request):
    email = request.data["email"]
    newpassword = my_random_string(8)
    try:
        user = User.objects.get(email= email)

        if user.is_staff == True:
            user.set_password(newpassword)
            user.save()
            updatedadmin = User.objects.get(is_staff=True)

            #send email
            msg = EmailMessage()
            msg['Subject'] = 'TInY admin password'
            msg['From'] = 'bulsu.tiny@gmail.com'
            msg['To'] = 'bulsu.tiny@gmail.com'

            msg.set_content('New Password: '+newpassword)
            msg.add_alternative("""\
            <!DOCTYPE html>
            <html>
                <head>
                    <style>
                        *{
                            padding:0;
                            margin:0;
                            box-sizing:border-box;
                            font-family: sans-serif;
                        }
                        .container{
                            background: #7d1b1c;
                            color: white;
                            padding: 10px 5px;
                            width: 200px;
                            text-align: center;
                            margin-top: 10px;
                            margin-bottom: 40px;
                        }
                        i{
                            color: rgb(70, 70, 70);
                        }
                    </style>
                </head>
                <body>
                    <h2>Your new password is</h2>
                    <div class="container">
                        <h1>"""+newpassword+ """</h1>
                    </div>

                    <i>Note: After logging-in using this password, it is best to change your password.</i>
                </body>
            </html>
            """, subtype='html')


            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("bulsu.tiny@gmail.com", "qvbioekrgdfrqvho")
                smtp.send_message(msg)

            ##sending response
            return Response({
                'id': updatedadmin.id, 
                'new_password': newpassword,
            })
        else:
            return Response({"error": "Email is incorrect..!!!"})

    
    except:
        return Response({'result': 'Server Error'})

########################

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def contactDevs(request):
    try:
        email = request.data["email"]
        name = request.data["name"]
        message = request.data["message"]

        #send email
        msg = EmailMessage()
        msg['Subject'] = 'Someone querying about TInY API'
        msg['From'] = 'bulsu.tiny@gmail.com'
        msg['To'] = 'dawn.bugay@gmail.com'

        msg.set_content('Sender Name: {} \n Sender Mailing Address: {} \n Message: {}'.format(name, email, message))


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("bulsu.tiny@gmail.com", "qvbioekrgdfrqvho")
            smtp.send_message(msg)

        ##sending response
        return Response({
            'Message': "Sent Success", 
        })
    except:
        return Response({'result': 'Server Error'})

##########################



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
def updateExecutive(request):
    try:
        id = request.data["id"]
        name = request.data["name"]

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
def updateDean(request):
    try:
        id = request.data["id"]
        name = request.data["name"]

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
def updatePopulation(request,):
    try:
        id= request.data["id"]
        student_population = request.data["student_population"]

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


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def getContacts(request):
    contact = Contact.objects.all().order_by('id')
    serializer = ContactSerializer(contact, many=True)
    return Response(serializer.data)

@api_view(['PATCH',])
@permission_classes((IsAuthenticated,))
def updateContact(request):
    try:
        id =  request.data['id']
        email =  request.data['email']
        facebook =  request.data['facebook']
        landline =  request.data['landline']
        college_secretary =  request.data['college_secretary']

        Contact.objects.filter(id=id).update(
            email=email,
            facebook = facebook,
            landline = landline,
            college_secretary = college_secretary
        )

        contact = Contact.objects.get(id=id)
        return Response({"MESSAGE": "BASTA SUCCESS YAN"})
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
def addCalendarEvent(request):
    # ${info.event}/${info.date_start}/${info.date_end}/${info.remark}/${info.name}/${encodeURIComponent(info.color)}
    event = request.data["event"]
    date_start = request.data["date_start"]
    date_end = request.data["date_end"]
    remark = request.data["remark"]
    name = request.data["name"]
    color = request.data["color"]
    
    
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
def updateCalendarEvent(request, id):
    remark = request.data["detail"]

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




######bot config######

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getChatbotSettings(request):
    settings = ChatbotSettings.objects.all()

    serializer = ChatbotSettingsSerializer(settings, many=True)
    return Response(serializer.data)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
def updateChatbotSettings(request):
    try:
        key = request.data['key']
        is_disable = request.data['is_disable']

        ChatbotSettings.objects.filter(key=key).update(
            is_disable=is_disable)
        setting = ChatbotSettings.objects.get(key=key)

        return Response({'key': setting.key, 'message': setting.message, 'is_disable': setting.is_disable})
    except:
        return Response({'MESSAGE': 'ID NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
def updateIntroMessage(request):
    try:
        new_message = request.data['message']

        ChatbotSettings.objects.filter(key="intro_message").update(
            message=new_message)

        return Response({"message": "success"})
    except:
        return Response({'MESSAGE': 'ID NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)