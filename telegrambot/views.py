from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from scales.utils import scale_string
from programs.models import Program
from django.utils.translation import gettext as _
from datetime import datetime, date
from .models import TelegramAccount, VerificationCode

def menu(request, id):
    ta = TelegramAccount.objects.filter(id_telegram =id).first()
    response = {}
    response['success'] = True
    if ta:
        response['options'] = [_('program')]
    else:
        response['options'] = [_('registry')]
    return JsonResponse(response)  #, safe=False    

def verification(request, id, code):
    vc = get_object_or_404(VerificationCode,pk=code)
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