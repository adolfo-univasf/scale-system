from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MinistryRegisterForm
from accounts.models import User
from ministries.models import Ministry,Function
from . import utils

@login_required
def dashboard(request):
    template_name = 'ministries/dashboard.html'
    context = {}
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    return render(request, template_name, context)

@login_required
def all(request):
    template_name = 'ministries/all.html'
    context = {}
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    context['ministries'] = Ministry.objects.all()
    return render(request, template_name, context)

@login_required
def description(request, ministry):
    template_name = 'ministries/description.html'
    context = {}
    try:
        context['ministry'] = Ministry.objects.get(slug = ministry)
    except Ministry.DoesNotExist:
        context['ministry'] = None

    context['user'] = request.user
    context['functions'] = context['ministry'].get_functions(request.user)
    context['not_functions'] = context['ministry'].get_not_functions(request.user)
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    
    return render (request, template_name, context)

@login_required
def edit(request, ministry):
    template_name = 'ministries/edit.html'
    success = False
    mn = Ministry.objects.get(slug = ministry)
    if request.method=='POST':
        form = MinistryRegisterForm(request.POST, instance = mn)
        form.set_options(User.objects.all())
        if form.is_valid():
            form.save()
            success = True
    else:
        form = MinistryRegisterForm(instance = mn, options=User.objects.all())
    context = {'form': form, 'success': success}
    context['ministry'] = mn
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    return render(request, template_name, context)

@login_required
def register(request):
    template_name = 'ministries/register.html'
    success = False
    if request.method=='POST':
        form = MinistryRegisterForm(request.POST)
        form.set_options(User.objects.all())
        if form.is_valid():
            form.save()
            success = True
    else:
        form = MinistryRegisterForm(options=User.objects.all())
    context = {'form': form, 'success': success}
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    return render(request, template_name, context)