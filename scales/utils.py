from ministries.models import Function,Ministry
from programs.models import Program,ProgramTime
from accounts.models import User
from django.utils.translation import gettext as _
from django.db.models import Q
from functools import reduce
#import pandas as pd
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

def transform_options(users):
    ret = []
    for us in users:
        ret.append(us.get_full_name())
    return ret

def scale_function(function: Function):
    return ProgramTime.objects.filter(function = function, 
                program__date__gte = datetime.date.today()
            ).order_by('program__date','time')

def scale_user(user: User):
    ret = list(ProgramTime.objects.filter(person = user, 
                program__date__gte = datetime.date.today()
            ).order_by('program__date','time'))
    if not ret:
        return []
    def m (x):
        return [{'program':x.program,'functions':[x]}]
    def r(a, x):
        for i in a:
            if x[0]['program'] == i['program']:
                i['functions']+=x[0]['functions']
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
            ret+= str(ps)+('* ' if sc.conf(ps) else '') + ', '
        ret = ret[:-2] + '\n'
    ret += "\n * - "+ _("not confirmmed functions")
    return ret

def scale_program_string(program:Program, markdown = False):
    sca = scale(program)
    ret = ('*' if markdown else '') + _("Program of") + " " + str(program) +('*' if markdown else '')+ "\n\n" 
    ret += ('```' if markdown else '')+_('Time')+('```' if markdown else '') +'\t'+('```' if markdown else '')+_('Function')+('```' if markdown else '')+ "\t\t" + ('```' if markdown else '')+_("People")+('```' if markdown else '') + "\n"
    for sc in sca:
        person = sc.person.get_queryset()
        ret += ('_' if markdown else '')+ (sc.time.strftime("%H:%M")if sc.time else '-----')+"\t" + ('_' if markdown else '') + ('_' if markdown else '')+sc.name() + ('_' if markdown else '')+' \t'
        for ps in person:
            ret+= str(ps) + ('* ' if sc.conf(ps) else '') + ', '
        ret = ret[:-2] + '\n'
    ret += "\n * - "+ _("not confirmmed functions")
    return ret

def scale_user_string(user:User, markdown = False):
    sca = scale(user)
    ret = ('*' if markdown else '') + _("Schedule of") + " " + str(user) +('*' if markdown else '')+ "\n\n" 
    ret += ('```' if markdown else '')+_("Date")+('```' if markdown else '') + "\t\t\t\t" + ('```' if markdown else '')+_("Functions")+('```' if markdown else '') + "\n"
    for sc in sca:
        ret += ('_' if markdown else '')+str(sc['program']) + ('_' if markdown else '')+"\t"
        for fn in sc['functions']:
            ret+= str(fn.function) + ('' if fn.conf(user) else '* ') + ', '
        ret = ret[:-2] + '\n'
    ret += "\n * - "+ _("not confirmmed functions")
    return ret

def scale_string(ob, markdown = False):
    if isinstance(ob,Function):
        return scale_function_string(ob, markdown)
    if isinstance(ob,User):
        return scale_user_string(ob, markdown)
    if isinstance(ob,Program):
        return scale_program_string(ob, markdown)
    return None

def scale_function_df(function:Function):
    sca = scale(function)
    dct = []
    for s in sca:
        c = {}
        c['date'] = str(s.program)
        c['desc'] = s.desc
        c['person'] = list(map(lambda x: str(x), s.person.get_queryset()))
        c['n_confirmmed'] = list(map(lambda x: str(x), s.n_confirmmed()))
        dct.append(c)
#    return pd.DataFrame(dct)

def scale_program_df(program:Program):
    sca = scale(program)
    dct = []
    for s in sca:
        c = {}
        c['time'] = s.time
        c['desc'] = s.desc
        c['person'] = list(map(lambda x: str(x), s.person.get_queryset()))
        c['n_confirmmed'] = list(map(lambda x: str(x), s.n_confirmmed()))
        dct.append(c)
#    return pd.DataFrame(dct)

def scale_user_df(user:User):
    sca = scale(user)
    dct = []
    for s in sca:
        c = {}
        c['date'] = str(s['program'])
        c['functions'] = list(map(lambda x: str(x.function), s['functions']))
        c['n_confirmmed'] = reduce(lambda a,x: a+x ,
            map(lambda x: [] if x.conf(user) else [str(x)], c['functions']))
        dct.append(c)
    #return pd.DataFrame(dct)

def scale_df(ob):
    if isinstance(ob,Function):
        return scale_function_df(ob)
    if isinstance(ob,User):
        return scale_user_df(ob)
    if isinstance(ob,Program):
        return scale_program_df(ob)
    return None

def function_list(user:User):
    #funções com este usuario na equipe
    functions = list(Function.objects.filter(people = user))
    #funções com este usuario como lider
    def m(x):
        return list(Function.objects.filter(ministry = x))
    def r(a,x):
        for i in x:
            if i not in a:
                a.append(i)
        return a    
    mn = Ministry.objects.filter(leader = user)
    mn = reduce(r,map(m,mn))
    #funções com este usuario citado na escala
    def m(x):
        return [x.func()]
    pt = ProgramTime.objects.filter(person = user, 
        program__date__gte = datetime.date.today())
    pt = reduce(r,map(m,pt))
    #juntando todos
    def m(x):
        return [x]
    function = reduce(r,map(m,functions + mn + pt))
    #print(function)
    return None

def program_list(user:User):
    pt = ProgramTime.objects.filter(person = user, 
        rogram__date__gte = datetime.date.today())
    def m(x):
        return [x.program]
    def r(a,x):
        for i in x:
            if i not in a:
                a.append(i)
        return a
    return reduce(r,map(m,pt))

def confirmation_list(user:User):
    pt = ProgramTime.objects.filter(person = user, 
        program__date__gte = datetime.date.today())
    cf = list(pt.filter(confirmmed = user))
    pt = list(pt)
    return list(filter(lambda x: x not in cf, pt))
    
def next_program(user):
    if len(function_list(user)) > 0:
        return Program.objects.filter(date__gte = datetime.date.today()).first()
"""
from programs.utils import *
user = User.objects.get(pk=1)
program = Program.objects.get(pk=20)
function = Function.objects.get(pk=9)

"""