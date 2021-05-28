from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MinistryRegisterForm
from accounts.models import User
from ministries.models import Ministry,Function

@login_required
def dashboard(request):
    template_name = 'ministries/dashboard.html'
    return render(request, template_name)

@login_required
def description(request, ministry):
    template_name = 'ministries/description.html'
    context = {}
    context['ministry'] = Ministry.objects.get(slug = ministry)
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
    return render(request, template_name, context)