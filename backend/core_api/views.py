from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from rest_framework import viewsets

from .models import Race, Result
from .serializers import RaceSerializer, ResultSerializer

class RaceViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


# test frontend views
def demo(request):
  template = loader.get_template('demo.html')
  races = Race.objects.all().values()
  context = {
     "races": races
  }
  return HttpResponse(template.render(context, request))

def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())