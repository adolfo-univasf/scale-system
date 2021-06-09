from .models import Program, ProgramTime
from datetime import date, datetime
from django.utils.translation import gettext as _

def template_program(template: Program):#, date:date
    #template = Program.objects.get(pk=7)
    program = Program()
    program.type_name = template.type_name
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

def programs_string(n=None):
    l = next_programs()
    if n is None:
        ret = _("Programs\n\n")
        for i,d in zip(range(len(l)),l):
            ret += "\t{} - {}\n".format(str(i+1),str(l))
        return ret
    elif n<= len(l) and n>0 :
        return l[n]

def loopverify(programtimes):
    for pt in programtimes:
        print("Olhando {}".format(str(pt)))
        if not pt.function:
            ptemp = pt.lookup
            while ptemp and ptemp!=pt and not ptemp.function:
                print("Tem Lookup com {}".format(str(ptemp)))
                ptemp = ptemp.lookup
            if ptemp == pt:
                print("Tem Lookup Conflitante com {}".format(str(ptemp)))
                pt.lookup = None
                pt.save()

def use_as_template(program: Program):#, date:date
    #template = Program.objects.get(pk=7)

    last_template = Program.objects.filter(type_name = program.type_name, date = None).first()
    if last_template:
        last_template.delete()

    template = Program()
    template.type_name = program.type_name
    #program.date = date
    template.transmission = program.transmission
    template.room = program.room
    template.image = program.image
    template.presential = program.presential
    template.iscription = program.iscription
    template.description = program.description
    template.save()
    program_times = list(ProgramTime.objects.filter(program = program))
    template_times = []
    for pt in program_times:
        tt = ProgramTime()
        tt.program = template
        tt.function = pt.function
        tt.desc = pt.desc
        tt.time = pt.time
        tt.save()
        template_times.append(tt)
    for tt, pt in zip (template_times,program_times):
        if(pt.lookup):
            tt.lookup = program_times[template_times.index(pt.lookup)]
            tt.save()
    return template#, program_times