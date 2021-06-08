from django.shortcuts import render
from django.http import JsonResponse
from scales.utils import scale_string
from programs.models import Program
from django.utils.translation import gettext as _
from datetime import datetime, date

def program (request):
    pg = list(Program.objects.filter(date__gte = date.today()))
    pg = list(filter(lambda x: x.enddatetime > datetime.now(), pg))
    if pg:
        pg = pg[0]
        response = {}
        response['success'] = True
        response['name'] = str(pg)
        response['date'] = str(pg.date)
        response['program'] = scale_string(pg)
        return JsonResponse(response)  #, safe=False
    else:
        response = {}
        response['success'] = False
        response['message'] = _("There is no next program")
        return JsonResponse(response)  #, safe=False