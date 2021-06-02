from django.shortcuts import render, redirect, get_object_or_404
from ministries.utils import my_functions, my_leader_functions
from .utils import scale as get_scale
from django.contrib.auth.decorators import login_required, permission_required
from ministries.models import Function

@login_required
def dashboard(request):
    template_name = "scales/dashboard.html"

    context = {}
    context['functions'] = my_functions(request.user)
    context['leader_functions'] = my_leader_functions(request.user)
    context['schedule'] = get_scale(request.user)
    return render(request, template_name, context)

@login_required
def scale(request, function):
    template_name = "scales/scale.html"
    fn = get_object_or_404(Function, pk = function)
    context = {}

    context['function'] = fn
    context['functions'] = my_functions(request.user)
    context['leader_functions'] = my_leader_functions(request.user)
    context['leader'] = fn.ministry.is_leader(request.user)
    context['scale'] = get_scale(fn)
    print(get_scale(fn))
    return render(request, template_name, context)

@login_required
def confirm(request, programtime):
    pass