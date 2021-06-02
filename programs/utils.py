from .models import Program, ProgramTime
from datetime import date, datetime

def template_program(template: Program):#, date:date
    #template = Program.objects.get(pk=7)
    program = Program()
    program.name = template.name
    #program.date = date
    program.transmission = template.transmission
    program.room = template.room
    program.image = template.image
    program.presential = template.presential
    program.iscription = template.iscription
    program.description = template.description
    program.save()
    template_times = list(ProgramTime.objects.filter(program = template))
    program_times = []
    for tt in template_times:
        pt = ProgramTime()
        pt.program = program
        pt.function = tt.function
        pt.desc = tt.desc
        pt.time = tt.time
        pt.save()
        program_times.append(pt)
    for tt, pt in zip (template_times,program_times):
        if(tt.lookup):
            pt.lookup = program_times[template_times.index(tt.lookup)]
            pt.save()
    return program#, program_times

def all_programs():
    return Program.objects.filter(date__isnull = False).order_by("-date")

def next_programs():
    programs = list(Program.objects.filter(date__isnull = False, date__gte = date.today()).order_by("date"))
    programs = list(filter(lambda x: x.datetime > datetime.now(), programs))
    return programs

def past_programs():
    programs = list(Program.objects.filter(date__isnull = False, date__lt = date.today()).order_by("-date"))
    programs = list(filter(lambda x: x.enddatetime < datetime.now(), programs))
    return programs

def resume_programs():
    return Program.objects.filter(date__gte = date.today())[:3]
