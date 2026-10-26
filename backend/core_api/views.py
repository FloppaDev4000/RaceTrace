from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from io import StringIO

from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.core.management.base import CommandError

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

@require_POST
def callGetRaces(request):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "error": "Please log in."}, status=401)
    if not (request.user.is_active and request.user.is_staff):
        return JsonResponse({"ok": False, "error": "Permission denied."}, status=403)
    out = StringIO()
    try:
        call_command("collect_races", stdout=out)
    except CommandError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)
    return JsonResponse({"ok": True, "output": out.getvalue()})