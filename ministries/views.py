from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext as _
from django.http import JsonResponse
from .forms import MinistryRegisterForm, FunctionRegisterForm
from accounts.models import User
from ministries.models import Ministry, Function
from core.forms import ConfirmForm
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
    context['ministry'] = get_object_or_404(Ministry, slug=ministry)

    context['user'] = request.user
    context['functions'] = context['ministry'].get_functions(request.user)
    context['not_functions'] = context['ministry'].get_not_functions(
        request.user)
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    context['leader'] = context['ministry'].is_leader(request.user)

    return render(request, template_name, context)


@login_required
@permission_required('ministries.change_ministry')
def edit(request, ministry):
    template_name = 'ministries/edit.html'
    success = False
    mn = get_object_or_404(Ministry, slug=ministry)

    if mn.leader.filter(pk=request.user.pk).first() is None:
        return redirect('ministries:description', ministry)

    if request.method == 'POST':
        form = MinistryRegisterForm(request.POST, instance=mn)
        form.set_options(User.objects.all())
        if form.is_valid():
            form.save()
            success = True
    else:
        form = MinistryRegisterForm(instance=mn)
        form.set_options(User.objects.all())
    context = {'form': form, 'success': success}
    context['ministry'] = mn
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    return render(request, template_name, context)


@login_required
def leave(request, ministry):
    mn = get_object_or_404(Ministry, slug=ministry)
    us = mn.leader.filter(pk=request.user.pk).first()
    context = {}
    if us:
        mn.leader.remove(us)
    return redirect('ministries:description', ministry)


@login_required
def leave_function(request, ministry, function):
    fn = get_object_or_404(Function, pk=function)
    us = fn.people.filter(pk=request.user.pk).first()
    context = {}
    if us:
        fn.people.remove(us)
    return redirect('ministries:description', ministry)


@login_required
def join_function(request, ministry, function):
    fn = get_object_or_404(Function, pk=function)
    us = fn.people.filter(pk=request.user.pk).first()
    context = {}
    if not us:
        fn.people.add(request.user)
    return redirect('ministries:description', ministry)


@login_required
@permission_required('ministries.delete_function')
def delete_function(request, ministry, function):
    template_name = 'delete.html'
    # ve se função existe
    fn = get_object_or_404(Function, pk=function)
    # ve se o usuario é lider no ministério da função
    if not fn.ministry.get_leader().filter(pk=request.user.pk).first():
        return redirect('ministries:description', ministry)
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            fn.delete()
            return redirect('ministries:description', ministry)
    else:
        form = ConfirmForm()
    context = {'form': form, 'title': _("Delete the Function: ") + str(fn)}
    return render(request, template_name, context)


@login_required
@permission_required('ministries.add_ministry')
def register(request):
    template_name = 'ministries/register.html'
    success = False

    if request.method == 'POST':
        form = MinistryRegisterForm(request.POST)
        form.set_options(User.objects.all())
        if form.is_valid():
            form.save()
            success = True
    else:
        form = MinistryRegisterForm()
        form.set_options(User.objects.all())
    context = {'form': form, 'success': success}
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    return render(request, template_name, context)


@login_required
@permission_required('ministries.add_function')
def register_function(request, ministry):
    template_name = 'ministries/register_function.html'
    success = False

    mn = get_object_or_404(Ministry, slug=ministry)

    if mn.leader.filter(pk=request.user.pk).first() is None:
        return redirect('ministries:description', ministry)

    if request.method == 'POST':
        form = FunctionRegisterForm(request.POST, ministry=mn)
        form.set_options(options_people=User.objects.all(),
                         options_overload=Function.objects.all())
        if form.is_valid():
            form.save()
            return redirect('ministries:description', ministry)
    else:
        form = FunctionRegisterForm(ministry=mn)
        form.set_options(options_people=User.objects.all(),
                         options_overload=Function.objects.all())
    context = {'form': form, 'success': success, 'ministry': mn}
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    return render(request, template_name, context)

@login_required
@permission_required('ministries.change_function')
def edit_function(request, ministry, function):
    template_name = 'ministries/edit_function.html'
    success = False
    mn = get_object_or_404(Ministry, slug=ministry)
    fn = get_object_or_404(Function, pk=function)

    if mn.leader.filter(pk=request.user.pk).first() is None:
        return redirect('ministries:description', ministry)

    if request.method == 'POST':
        form = FunctionRegisterForm(request.POST, instance=fn,ministry=mn)
        form.set_options(options_people=User.objects.all(),
                         options_overload=Function.objects.all())
        if form.is_valid():
            form.save()
            success = True
    else:
        form = FunctionRegisterForm(instance=fn,ministry=mn)
        form.set_options(options_people=User.objects.all(),
                         options_overload=Function.objects.all())
    context = {'form': form, 'success': success}
    context['ministry'] = mn
    context['function'] = fn
    context['my_engaged'] = utils.my_engaged(request.user)
    context['my_ministries'] = utils.my_ministries(request.user)
    return render(request, template_name, context)    

@login_required
def all_functions_select_json(request):
    functions = Function.objects.all()
    functions = list(map(lambda f:{'key':f.pk,'value':f.desc},functions))
    return JsonResponse(functions)