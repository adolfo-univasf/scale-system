from django.shortcuts import render
from .models import Program,ProgramTime
from datetime import datetime, date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext as _
from django.urls import reverse
from . import utils
from .forms import ProgramRegisterForm,UseTemplateForm

# Create your views here.
def dashboard(request):
    template_name = "programs/dashboard.html"
    pg = list(Program.objects.filter(date__gte = date.today()))
    pg = list(filter(lambda x: x.enddatetime > datetime.now(), pg))
    if pg:
        return redirect('programs:description', pg[0].pk)
    else:
        return render(request, template_name)


    
@login_required
@permission_required('programs.add_program')
def register(request):
    template_name = 'programs/register.html'

    form = ProgramRegisterForm()
    form2 = UseTemplateForm()

    if request.method == 'POST':
        try:
            if(request.POST['name']):
                form = ProgramRegisterForm(request.POST)
                if form.is_valid():
                    pg = form.save()
                    return redirect('programs:description', pg.pk)
        except KeyError as identifier:
            sel = int(request.POST['templates'])
            template = get_object_or_404(Program, pk=sel)
            print(template)
            pg = utils.template_program(template)
            return redirect('programs:edit', pg.pk)
        
        
    context = {'form': form, 'form2': form2}
    context['resume'] = utils.resume_programs()
    return render(request, template_name, context)

def all(request):
    template_name = "programs/all.html"
    programs = utils.all_programs()
    context = {'programs':programs}
    context['link_page'] = reverse('programs:all')
    context['title_page'] = _("All Programs")
    context['resume'] = utils.resume_programs()
    return render(request, template_name, context)

def past(request):
    template_name = "programs/all.html"
    programs = utils.past_programs()
    context = {'programs':programs}
    context['link_page'] = reverse('programs:past')
    context['title_page'] = _("Past Programs")
    context['resume'] = utils.resume_programs()
    return render(request, template_name, context)

def next(request):
    template_name = "programs/all.html"
    programs = utils.next_programs()    
    context = {'programs':programs}
    context['link_page'] = reverse('programs:next')
    context['title_page'] = _("Next Programs")
    context['resume'] = utils.resume_programs()
    return render(request, template_name, context)


def description(request, program):
    template_name = "programs/description.html"
    pg = get_object_or_404(Program.objects,pk=program)
    context = {'program':pg}
    context['resume'] = utils.resume_programs()
    return render(request, template_name, context)

def program(request, program):
    template_name = "programs/program.html"
    pg = get_object_or_404(Program.objects,pk=program)
    pt = ProgramTime.objects.filter(program = pg)
    context = {'program':pg, "programtime":pt}
    context['resume'] = utils.resume_programs()
    return render(request, template_name, context)

@login_required
@permission_required('programs.change_program')
def edit(request, program):
    template_name = 'programs/edit.html'
    pg = get_object_or_404(Program, pk=program)

    if request.method == 'POST':
        form = ProgramRegisterForm(request.POST,instance=pg)
        if form.is_valid():
            form.save()
            return redirect('programs:description', pg.pk)
    else:
        form = ProgramRegisterForm(instance=pg)
    context = {'form': form}
    context['program'] = pg
    context['resume'] = utils.resume_programs()

    return render(request, template_name, context)