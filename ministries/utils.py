from accounts.models import User
from .models import Ministry, Function
from programs.models import ProgramTime
from django.utils.translation import gettext as _
from functools import reduce

def my_engaged(user):
    def m(x):
        return [x.ministry]
    def r(x,a):
        if x[0] and x[0] not in a:
            a.append(x[0])
        return a
    functions = list(Function.objects.filter(people = user))

    #funções que eu não estou na equipe mas fui colocado na escala
    prog = ProgramTime.objects.filter(person = user)
    for pg in prog:
        functions.append(pg.function)

    if functions:
        return reduce(r,map(m,functions))
    else:
        return []
def my_ministries(user):
     return Ministry.objects.filter(leader=user)

def my_functions(user):
    def m(x):
        return [x]
    def r(x,a):
        if x[0] and x[0] not in a:
            a.append(x[0])
        return a
    functions = list(Function.objects.filter(people = user))

    #funções que eu não estou na equipe mas fui colocado na escala
    prog = ProgramTime.objects.filter(person = user)
    for pg in prog:
        functions.append(pg.function)
    
    if functions:
        return reduce(r,map(m,functions))
    else:
        return []

def my_leader_functions(user):
    return Function.objects.filter(ministry__leader = user)

def all_functcions(user):
    l = my_functions(user) + my_leader_functions(user)
    def m(x):
        return [x]
    def r(x,a):
        if x[0] and x[0] not in a:
            a.append(x[0])
        return a
    if l:
        return reduce(r,map(m,l))
    else:
        return []

def functions_string(user, n=None):
    l = all_functcions(user)
    if n is None:
        ret = _("Functions\n\n")
        for i,d in zip(range(len(l)),l):
            ret += "\t{} - {}\n".format(str(i+1),str(l))
        return ret
    elif n<= len(l) and n>0 :
        return l[n]