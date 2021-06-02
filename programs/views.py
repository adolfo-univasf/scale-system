from django.shortcuts import render
from .models import Program,ProgramTime
from datetime import datetime, date
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def dashboard(request):
    template_name = "programs/dashboard.html"
    pg = list(Program.objects.filter(date__gte = date.today()))
    pg = list(filter(lambda x: x.enddatetime > datetime.now(), pg))
    if pg:
        return redirect('programs:description', pg[0].pk)
    else:
        return render(request, template_name)


    
def register(request):
    pass
def all(request):
    pass
def description(request, program):
    template_name = "programs/description.html"
    pg = get_object_or_404(Program.objects,pk=program)
    context = {'program':pg}
    return render(request, template_name, context)

def program(request, program):
    template_name = "programs/program.html"
    pg = get_object_or_404(Program.objects,pk=program)
    pt = ProgramTime.objects.filter(program = pg)
    print(pt)
    context = {'program':pg, "programtime":pt}
    return render(request, template_name, context)