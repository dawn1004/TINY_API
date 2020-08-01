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
from .serializers import TinyResponseSerializer

from . models import Question, Calendar, userIntent
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


@api_view(['POST', ])
def createUser(request, username, password, name, intent):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(username=username,
                                            email='jlennon@beatles.com111',
                                            password=password)
            intent = userIntent(intent=intent, user=user)

            intent.save()
        except:
            return Response({'error': 'Username is already taken'})

    return Response({'username': password})
    # http://127.0.0.1:8000/tinyAPI/createUser/dawn11232123/124553/dawnhae/school related/


@api_view(['GET', ])
def adminLogin(request, username, password):
    admin = authenticate(request, username=username, password=password)
    if admin is not None:
        if admin.is_staff:
            return Response({'result': 'found', 'username': username, 'password': password})

    return Response({'result': 'not found'})
    # http://127.0.0.1:8000/tinyAPI/adminLogin/kishinki/dawn123741/
