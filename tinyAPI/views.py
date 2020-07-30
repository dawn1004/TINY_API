from django.shortcuts import render
from django.http import HttpResponse
import numpy
import random
import datetime

from .modelBot import model as modelo

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TinyResponseSerializer

from . models import Question, Calendar


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
