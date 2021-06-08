from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from scales.utils import scale_string
from ministries.utils import my_functions, my_leader_functions
from programs.models import Program
from django.utils.translation import gettext as _
from datetime import datetime, date
from .models import TelegramAccount, VerificationCode
from django.contrib.auth.decorators import login_required
from core.forms import ConfirmForm
from django.db.utils import IntegrityError

@login_required
def dashboard(request):
    template_name = "telegrambot/dashboard.html"
    user = request.user
    tl = TelegramAccount.objects.filter(user=user)
    vc = list(VerificationCode.objects.filter(user=user))
    vc = list(filter(lambda x: not (x.confirmed == True), vc))
    context = {}
    context['telegram'] = tl
    if len(vc) > 0:
        context['codes'] = vc
    return render(request, template_name,context)

@login_required
def generate(request):
    vc = VerificationCode()
    vc.user = request.user
    vc.save()
    return redirect('telegrambot:dashboard')

@login_required
def delete(request, id):
    template_name = 'delete.html'
    # ve se função existe
    tl = get_object_or_404(TelegramAccount, id_telegram=id)
    # ve se o usuario é lider no ministério da função
    if not tl.user == request.user:
        return redirect('telegrambot:dashboard')
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            tl.delete()
            return redirect('telegrambot:dashboard')
    else:
        form = ConfirmForm()
    context = {'form': form, 'title': _("Delete the Telegram Account: ") + str(tl)}
    return render(request, template_name, context)

def menu(request, id):
    ta = TelegramAccount.objects.filter(id_telegram =id).first()
    response = {}
    response['success'] = True
    if ta:
        response['options'] = ['program', 'scale', 'schedule']
    else:
        response['options'] = ['register']
    return JsonResponse(response)  #, safe=False

def register(request, id, code):
    vc = VerificationCode.objects.filter(pk=code).first()
    response = {}
    print(vc.confirmed)
    if vc and not vc.confirmed:
        ta = TelegramAccount()
        ta.user = vc.user
        vc.confirmed = True
        vc.save()
        ta.id_telegram = id
        try:
            ta.save()
        except IntegrityError as identifier:
            response['success'] = False
            response['message'] = _("This telegram account is already registred")
            return JsonResponse(response)  #, safe=False
        response['success'] = True
        response['message'] = _("Registration completed successfully")
        return JsonResponse(response)  #, safe=False
    else:
        response['success'] = False
        response['message'] = _("Invalid Code")
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

def schedule (request, id):
    ta = TelegramAccount.objects.filter(id_telegram =id).first()
    if ta:
        user = ta.user
        response = {}
        response['success'] = True
        response['user'] = str(user.get_full_name())
        response['schedule'] = scale_string(user)
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
def scale(request, id, code):
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
            if fn.pk == code:
                response['success'] = True
                response['function'] = str(fn)
                response['function_id'] = code
                response['scale'] = scale_string(fn)
                return JsonResponse(response)  #, safe=False
    else:
        response = {}
        response['success'] = False
        response['message'] = _("Telegram Id not registred")
    return JsonResponse(response)  #, safe=False