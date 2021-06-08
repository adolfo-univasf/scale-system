from django.shortcuts import render
from django.http import JsonResponse
from scales.utils import scale_string
from programs.models import Program
from django.utils.translation import gettext as _
from datetime import datetime, date
from .models import TelegramAccount, VerificationCode

def verification(request, id, code):
    vc = VerificationCode.objects.get(pk=code)
    ta = TelegramAccount()
    ta.user = vc.user
    ta.id_telegram = id
    response = {}
    response['success'] = True
    response['message'] = _("Registration completed successfully")
    return JsonResponse(response)  #, safe=False

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