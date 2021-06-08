from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from scales.utils import scale_string
from ministries.utils import my_functions, my_leader_functions
from programs.models import Program
from django.utils.translation import gettext as _
from datetime import datetime, date
from .models import TelegramAccount, VerificationCode

def menu(request, id):
    ta = TelegramAccount.objects.filter(id_telegram =id).first()
    response = {}
    response['success'] = True
    if ta:
        response['options'] = ['program', 'scale']
    else:
        response['options'] = ['register']
    return JsonResponse(response)  #, safe=False

def register(request, id, code):
    vc = get_object_or_404(VerificationCode,pk=code)
    ta = TelegramAccount()
    ta.user = vc.user
    ta.id_telegram = id
    ta.save()
    response = {}
    response['success'] = True
    response['message'] = _("Registration completed successfully")
    return JsonResponse(response)  #, safe=False

def program (request, id):
    ta = TelegramAccount.objects.filter(id_telegram =id).first()
    if ta:
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
    else:
        response = {}
        response['success'] = False
        response['message'] = _("Telegram Id not registred")
        return JsonResponse(response)  #, safe=False
def scale_list (request, id):
    ta = TelegramAccount.objects.filter(id_telegram =id).first()
    response = {}
    if ta:
        us = ta.user
        functions = my_functions(us)
        ld_func = my_leader_functions(us)
        for fn in ld_func:
            if fn not in functions:
                functions.append(fn)
        response['success'] = True
        response['options'] = list(map(lambda x:{'pk':x.pk,'name':str(x)}, functions))
        return JsonResponse(response)  #, safe=False
    else:
        response['success'] = False
        response['message'] = _("Telegram Id not registred")
        return JsonResponse(response)  #, safe=False
def scale(request, id, scale):
    ta = TelegramAccount.objects.filter(id_telegram =id).first()
    response = {}
    if ta:
        us = ta.user
        functions = my_functions(us)
        ld_func = my_leader_functions(us)
        for fn in ld_func:
            if fn not in functions:
                functions.append(fn)
        for fn in functions:
            if scale.pk == scale:
                response['success'] = True
                response['function'] = str(fn)
                response['function_id'] = scale
                response['scale'] = scale_string(fn)
                return JsonResponse(response)  #, safe=False
    else:
        response = {}
        response['success'] = False
        response['message'] = _("Telegram Id not registred")
    return JsonResponse(response)  #, safe=False