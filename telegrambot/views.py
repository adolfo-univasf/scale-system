from django.shortcuts import render
from django.http import JsonResponse
from scales.utils import scale_string
from programs.models import Program
from datetime import datetime, date

# Create your views here.

def program (request):
    pg = list(Program.objects.filter(date__gte = date.today()))
    pg = list(filter(lambda x: x.enddatetime > datetime.now(), pg))
    if pg:
        pg = pg[0]
        response = {}
        response['name'] = str(pg)
        response['date'] = str(pg.date)
        response['program'] = scale_string(pg)
        return JsonResponse(response)  #, safe=False
    else: