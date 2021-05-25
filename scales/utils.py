from scales.models import Function,Ministry,Program,ProgramTime
from accounts.models import User
from django.utils.translation import gettext as _
from functools import reduce
import datetime

def function_options(program_time : ProgramTime):
# try:
#     ProgramTime.objects.get(pk=1)
# except ProgramTime.DoesNotExist as identifier:
#     print("Essa momento não existe")
#   program_time = ProgramTime.objects.get(pk=3)
    options = list(program_time.function.people.get_queryset())

    #não é a melhor forma de fazer (list)
    #O ideal é utilizar o recurso difference (do queryset)
    # ele faz as requisições em sql diretamente no banco
    # mas não funciona em sqlite ou oracle
    # não consegui instalar o banco
    # pelo modelo de negócio, nesta função não será um problema 
    # ja que nunca será submetido a um volume de dados muito grande nesta parte
    times_on_program = list(ProgramTime.objects.filter(program = program_time.program))
    times_overload = list(program_time.function.overload.get_queryset())

    times_to_view = list(filter(lambda x: x.function not in times_overload, times_on_program))

    users_to_view = []
    for tv in times_to_view:
        users_to_view += list(tv.person.get_queryset())

    options = list(filter(lambda x: x not in users_to_view, options))

    return options
    
def new_program(template: Program, date:datetime.date):
    #template = Program.objects.get(pk=7)
    program = Program()
    program.name = template.name
    program.date = date
    program.save()
    template_times = ProgramTime.objects.filter(program = template)
    program_times = []
    for tt in template_times:
        pt = ProgramTime()
        pt.program = program
        pt.function = tt.function
        pt.lookup = tt.lookup
        pt.desc = tt.desc
        pt.time = tt.time
        program_times.append(pt)
    return program, program_times

def scale_function(function: Function):
    return ProgramTime.objects.filter(function = function, 
                program__date__gte = datetime.date.today()
            ).order_by('program__date','time')

def scale_user(user: User):
    ret = ProgramTime.objects.filter(person = user, 
                program__date__gte = datetime.date.today()
            ).order_by('program__date','time')

    def m (x):
        return [[x]]
    def r(a, x):
        for i in a:
            if x[0][0].program == i[0].program:
                i.append(x[0][0])
                return a
        a.append(x[0])
        return a
    return reduce(r,map(m,ret))

def scale_program(program: Program):
    return ProgramTime.objects.filter(program = program)

def scale(ob):
    if isinstance(ob,Function):
        return scale_function(ob)
    if isinstance(ob,User):
        return scale_user(ob)
    if isinstance(ob,Program):
        return scale_program(ob)
    return None

def scale_function_string(function:Function, markdown = False):
    sca = scale(function)
    ret = ('*' if markdown else '') + _("Scale of") + " " + function.name +('*' if markdown else '')+ "\n\n" 
    ret += ('```' if markdown else '')+_("Date")+('```' if markdown else '') + "\t\t\t\t" + ('```' if markdown else '')+_("People")+('```' if markdown else '') + "\n"
    for sc in sca:
        person = sc.person.get_queryset()
        ret += ('_' if markdown else '')+str(sc.program) + ('_' if markdown else '')+"\t"
        for ps in person:
            ret+= str(ps) + ', '
        ret = ret[:-2] + '\n'
    return ret

def scale_program_string(program:Program, markdown = False):
    sca = scale(program)
    ret = ('*' if markdown else '') + _("Program of") + " " + str(program) +('*' if markdown else '')+ "\n\n" 
    ret += ('```' if markdown else '')+_('Time')+('```' if markdown else '') +'\t'+('```' if markdown else '')+_('Function')+('```' if markdown else '')+ "\t\t" + ('```' if markdown else '')+_("People")+('```' if markdown else '') + "\n"
    for sc in sca:
        person = sc.person.get_queryset()
        ret += ('_' if markdown else '')+ (sc.time.strftime("%H:%M")if sc.time else '-----')+"\t" + ('_' if markdown else '') + ('_' if markdown else '')+sc.name() + ('_' if markdown else '')+' \t'
        for ps in person:
            ret+= str(ps) + ', '
        ret = ret[:-2] + '\n'
    return ret

def scale_user_string(user:User, markdown = False):
    sca = scale(user)
    ret = ('*' if markdown else '') + _("Schedule of") + " " + str(user) +('*' if markdown else '')+ "\n\n" 
    ret += ('```' if markdown else '')+_("Date")+('```' if markdown else '') + "\t\t\t\t" + ('```' if markdown else '')+_("Functions")+('```' if markdown else '') + "\n"
    for sc in sca:
        ret += ('_' if markdown else '')+str(sc[0].program) + ('_' if markdown else '')+"\t"
        for fn in sc:
            ret+= str(fn.function) + ', '
        ret = ret[:-2] + '\n'
    return ret

def scale_string(ob, markdown = False):
    if isinstance(ob,Function):
        return scale_function_string(ob, markdown)
    if isinstance(ob,User):
        return scale_user_string(ob, markdown)
    if isinstance(ob,Program):
        return scale_program_string(ob, markdown)
    return None

"""
from scales.utils import *
user = User.objects.get(pk=1)
program = Program.objects.get(pk=20)
function = Function.objects.get(pk=9)

"""